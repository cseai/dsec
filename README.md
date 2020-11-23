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

## Set up static directory and default files
To work properly `static_cdn` need to add at the very beginning of the working directory where `src` folder exist.
Sometimes it's need to add default file in a specific directory manually (Because it depends on the implementation in every django-app and file structure described in implementation).
Folder structure looks like:
```
static_cdn
├───media_root
│   └───accounts
│       └───user
│           └───image
└───static_root
```
Here `static_root` store all **static** files and `media_root` stores all **media** files.
Inside `media_root` folder, path pattern looks like:
```
media_root
└───<app_label>
    └───<model>
        └───<field_name>
```
In the previous case, `accounts` is `<app_label>`, `user` is `<model>` and `image` is `<field_name>` which was set at the model implementation time.
Inside the `<field_name>` directory more complicated file path could be set up. It's depend on implementation. There can have default file. In case of `user` model there has a default image inside the `image` directory named `default.png` which must be set to work the app properly.

Therefore, it is responsible to the developer to keep track on the implementation as well as static path.

## static_cdn
There can have file at the end of every directory.
Example: inside `image` directory there must have a `default.png` file.
```
static_cdn
├───media_root
│   ├───accounts
│   │   └───user
│   │       └───image
│   ├───products
│   │   ├───cuisine
│   │   │   └───image
│   │   └───product
│   │       └───image
│   └───vendors
│       └───store
│           └───logo
└───static_root
```