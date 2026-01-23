# import marimo as mo

# app = mo.App()


# @app.cell
# def _():
#     """
#     Environment + imports cell
#     """
#     import sys
#     import os
#     import pandas as pd
#     import marimo as mo

#     # 1. Path Setup: Ensure Python can find your 'ml' and 'ingestion' folders
#     # This logic looks 2 levels up from the current file
#     current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
#     project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    
#     if project_root not in sys.path:
#         sys.path.insert(0, project_root)

#     # 2. Import your custom module
#     # (Ensure ml/recommenders/playlist_generator.py exists)
#     from ml.recommenders.playlist_generator import generate_playlist
    
#     return generate_playlist, mo, pd, sys, os


# @app.cell
# def _(generate_playlist):
#     """
#     Run ML playlist generation
#     """
#     try:
#         # Generate the playlist
#         playlist_df = generate_playlist(
#             user_id="current_user",
#             playlist_size=15,
#         )
#         error = None
#     except Exception as e:
#         playlist_df = None
#         error = str(e)

#     return playlist_df, error


# @app.cell
# def _(playlist_df, error, mo):
#     """
#     Render UI
#     """
#     # 1. Initialize list of UI elements
#     ui_elements = [mo.md("# 🎶 Your Personalized Playlist")]

#     # 2. Logic to build the UI stack
#     if error:
#         ui_elements.append(
#             mo.callout(
#                 mo.md(f"**Error generating playlist:** `{error}`"), 
#                 kind="danger"
#             )
#         )

#     elif playlist_df is None or playlist_df.empty:
#         ui_elements.append(
#             mo.callout(
#                 mo.md("⚠️ No playlist generated yet. Try ingesting more data."),
#                 kind="warn"
#             )
#         )

#     else:
#         # Extract Persona
#         persona = playlist_df["persona"].iloc[0] if "persona" in playlist_df.columns else "Unknown"
        
#         ui_elements.append(mo.md(f"## 🧠 Current Listening Persona: **{persona}**"))

#         # Playlist Table
#         ui_elements.append(mo.md("## 🎧 Recommended Artists"))
        
#         # Select specific columns to keep the table clean
#         display_cols = ["artist", "similarity_score", "previous_plays"]
#         # Filter only columns that actually exist in the dataframe
#         valid_cols = [c for c in display_cols if c in playlist_df.columns]
        
#         ui_elements.append(
#             mo.ui.table(playlist_df[valid_cols])
#         )

#         # Explainability Section
#         ui_elements.append(mo.md("## Why these recommendations?"))
#         ui_elements.append(
#             mo.md("""
#             - **Similarity score**: How close this artist is to your recent listening sessions  
#             - **Previous plays**: How often you've listened before  
#             - **Persona rules**: Adapts novelty vs familiarity automatically
#             """)
#         )

#     # 3. CRITICAL: Return the stack to display it
#     return mo.vstack(ui_elements, gap=1.5)


# if __name__ == "__main__":
#     app.run()



@app.cell
def _():
    import os
    import sys
    
    # 1. Where does Python think we are?
    cwd = os.getcwd()
    
    # 2. What files are here?
    files = os.listdir(cwd)
    
    # 3. Can we see the 'ml' folder?
    ml_path = os.path.join(cwd, "ml")
    ml_exists = os.path.exists(ml_path)
    
    # 4. Can we see the 'ingestion' folder?
    ingest_path = os.path.join(cwd, "ingestion")
    ingest_exists = os.path.exists(ingest_path)

    print(f"📍 Current Folder: {cwd}")
    print(f"📂 Files found: {files}")
    print(f"🔎 'ml' folder exists? {'✅ YES' if ml_exists else '❌ NO'}")
    print(f"🔎 'ingestion' folder exists? {'✅ YES' if ingest_exists else '❌ NO'}")
    
    return