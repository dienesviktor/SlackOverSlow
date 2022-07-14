import os
import bcrypt
from werkzeug.utils import secure_filename
from markupsafe import Markup


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def save_image(data, image):
    if "title" in data:
        if image:
            file_name = secure_filename(image.filename)
            data["image"] = file_name
            image.save(os.path.join(f"{os.getcwd()}/static/images/questions/", file_name))
        else:
            data["image"] = None
    else:
        if image:
            file_name = secure_filename(image.filename)
            data["image"] = file_name
            image.save(os.path.join(f"{os.getcwd()}/static/images/answers/", file_name))
        else:
            data["image"] = None
    return data


def delete_image(data):
    if "title" in data[0]:
        if data[0]["image"] is not None:
            file_name = f"{os.getcwd()}/static/images/questions/{data[0]['image']}"
            if os.path.exists(file_name):
                os.remove(os.path.join(file_name))
    else:
        if data[0]["image"] is not None:
            file_name = f"{os.getcwd()}/static/images/answers/{data[0]['image']}"
            if os.path.exists(file_name):
                os.remove(os.path.join(file_name))


def highlight_search_result(data, searched):
    for item in data:
        for key, value in item.items():
            if key == "message" or key == "title":
                item[key] = Markup(item[key].lower().replace(f"{searched.lower()}", f"<mark>{searched}</mark>"))
    return data
