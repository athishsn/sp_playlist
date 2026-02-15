import marimo as mo
app = mo.App()

@app.cell
def _():
    return mo.md("# Marimo is rendering")

if __name__ == "__main__":
    app.run()
