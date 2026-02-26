import streamlit as st
import pandas as pd

from src.config import AppConfig
from src.io_utils import save_bytes_to_temp, safe_remove
from src.pipeline import analyze_call

cfg = AppConfig()

st.set_page_config(page_title="Emergency AI", page_icon="🚨", layout="wide")

st.title("🚨 Offline Emergency Call Triage & Guidance")
st.caption("Challenge 12 + 15: Prioritize emergency calls and generate context-aware emergency instructions (offline CPU).")

with st.expander("System Architecture (Offline)"):
    st.markdown(
        """
**Audio → Clean (16k mono) → Whisper STT → Situation & Emotion (rules) → Stress (signal) → Urgency fusion → Instruction**

- Works fully offline on CPU (no internet dependency)
- Produces explainable decisions (keyword hits + scoring breakdown)
- Supports single-call analysis and queue prioritization
"""
    )

tab1, tab2 = st.tabs(["Single Call", "Call Queue (Batch)"])


def level_badge(level: str, text: str):
    if level == "CRITICAL":
        st.error(text)
    elif level == "HIGH":
        st.warning(text)
    elif level == "MEDIUM":
        st.info(text)
    else:
        st.success(text)


def manual_review_flag(situation: str, s_conf: float, e_conf: float) -> bool:
    # Explainable, operator-friendly rule
    return (situation in {"UNKNOWN"}) or (s_conf < 0.55) or (e_conf < 0.55)


with tab1:
    st.subheader("Single Call Analysis")
    uploaded = st.file_uploader("Upload one audio file", type=["wav", "mp3", "m4a"], key="single")

    if uploaded:
        raw_path = None
        try:
            with st.spinner("Processing..."):
                suffix = "." + uploaded.name.split(".")[-1].lower()
                raw_path = save_bytes_to_temp(cfg, uploaded.read(), suffix=suffix)

                res = analyze_call(cfg, raw_path, filename=uploaded.name)
                manual_review = manual_review_flag(res.situation, res.s_conf, res.e_conf)

            st.audio(uploaded)

            st.subheader("Transcript")
            st.success(res.transcript if res.transcript else "No speech detected.")

            st.subheader("Analysis Results")
            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.markdown("### Situation")
                st.write(f"**{res.situation}**")
                st.caption(f"conf: {res.s_conf:.2f}")

            with c2:
                st.markdown("### Emotion")
                st.write(f"**{res.emotion}**")
                st.caption(f"conf: {res.e_conf:.2f}")

            with c3:
                st.markdown("### Stress (Audio)")
                st.write(f"**{res.stress:.1f}/100**")
                st.caption("signal-based proxy")

            with c4:
                st.markdown("### Urgency")
                st.progress(min(int(res.urgency), 100))
                level_badge(res.level, f"{res.urgency}/100 — {res.level}")

            if manual_review:
                st.warning("Manual review recommended (low confidence or unknown situation).")

            with st.expander("Why? (Explainability)"):
                st.write(
                    {
                        "keyword_hits": res.hits,
                        "scoring_breakdown": res.explain,
                        "manual_review": manual_review,
                    }
                )

            st.subheader("Emergency Instruction")
            st.success(res.instruction)

        except Exception as e:
            st.error(f"Error occurred: {e}")
        finally:
            safe_remove(raw_path)


with tab2:
    st.subheader("Call Queue (Batch Prioritization)")
    st.info("Tip: Upload 3 demo calls (CRITICAL / HIGH / MEDIUM) to showcase prioritization in 60 seconds.")

    uploaded_files = st.file_uploader(
        "Upload multiple audio files",
        type=["wav", "mp3", "m4a"],
        accept_multiple_files=True,
        key="batch",
    )

    if uploaded_files:
        results = []
        temp_paths = []

        try:
            with st.spinner("Processing batch..."):
                for f in uploaded_files:
                    suffix = "." + f.name.split(".")[-1].lower()
                    p = save_bytes_to_temp(cfg, f.read(), suffix=suffix)
                    temp_paths.append(p)
                    results.append(analyze_call(cfg, p, filename=f.name))

            # Sort by urgency DESC (queue prioritization)
            results.sort(key=lambda r: r.urgency, reverse=True)

            df = pd.DataFrame(
                [
                    {
                        "rank": i + 1,
                        "filename": r.filename,
                        "urgency": r.urgency,
                        "level": r.level,
                        "situation": r.situation,
                        "s_conf": round(r.s_conf, 2),
                        "emotion": r.emotion,
                        "e_conf": round(r.e_conf, 2),
                        "stress": round(r.stress, 1),
                        "manual_review": manual_review_flag(r.situation, r.s_conf, r.e_conf),
                        "transcript": r.transcript,
                        "instruction": r.instruction,
                    }
                    for i, r in enumerate(results)
                ]
            )

            st.subheader("Prioritized Queue")
            st.dataframe(df, use_container_width=True)

            st.download_button(
                "Download CSV report",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="emergency_call_queue_report.csv",
                mime="text/csv",
            )

            st.subheader("Top 3 Calls (Operator View)")
            top = results[:3]
            for r in top:
                mr = manual_review_flag(r.situation, r.s_conf, r.e_conf)
                st.markdown(f"### {r.filename}")
                level_badge(r.level, f"{r.urgency}/100 — {r.level} | {r.situation} | {r.emotion} | stress={r.stress:.1f}")
                if mr:
                    st.warning("Manual review recommended for this call.")
                st.write(r.transcript)
                st.success(r.instruction)
                with st.expander("Why?"):
                    st.write({"hits": r.hits, "breakdown": r.explain, "manual_review": mr})

        except Exception as e:
            st.error(f"Batch failed: {e}")
        finally:
            for p in temp_paths:
                safe_remove(p)