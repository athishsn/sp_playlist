import marimo

__generated_with = "0.19.4"
app = marimo.App()


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT * FROM
        """
    )
    return


if __name__ == "__main__":
    app.run()
