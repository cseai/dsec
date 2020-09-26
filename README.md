# DSEC

Delivery Service and E-Commerce (DSEC) system.

## Set up environment
Clone this repository and open terminal inside it's main directory.

Then create python virtual environment named `venv`:
```bash
    python -m venv venv
```
Activate venv (In windows 10):
```bash
    venv\Scripts\activate
```

After that move to the `src/` directory:
```bash
    cd src
```

And then install required packages using `pip` according to `requirements.txt` file:
```bash
    pip install -r requirements.txt
```

If everything goes write then you can run development server:
```bash
    python manage.py runserver
```
