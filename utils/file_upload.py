"""
==================================
MANGA GALLERY
FILE UPLOAD UTILS
==================================
"""

import os
import uuid

from werkzeug.utils import secure_filename


"""
==================================
ALLOWED EXTENSIONS
==================================
"""

ALLOWED_EXTENSIONS = {

    "jpg",

    "jpeg",

    "png",

    "webp"

}


"""
==================================
CHECK EXTENSION
==================================
"""

def allowed_file(

    filename

):

    return (

        "." in filename

        and filename.rsplit(

            ".",

            1

        )[1].lower()

        in ALLOWED_EXTENSIONS

    )


"""
==================================
GENERATE FILE NAME
==================================
"""

def generate_filename(

    filename

):

    extension = filename.rsplit(

        ".",

        1

    )[1].lower()

    return (

        f"{uuid.uuid4()}.{extension}"

    )
    
    """
==================================
SAVE FILE
==================================
"""

def save_file(

    file,

    upload_folder

):

    filename = secure_filename(

        file.filename

    )

    filename = generate_filename(

        filename

    )

    os.makedirs(

        upload_folder,

        exist_ok=True

    )

    file_path = os.path.join(

        upload_folder,

        filename

    )

    file.save(

        file_path

    )

    return file_path


"""
==================================
CHECK FILE SIZE
==================================
"""

def validate_file_size(

    file,

    max_size=10 * 1024 * 1024

):

    file.seek(

        0,

        os.SEEK_END

    )

    size = file.tell()

    file.seek(

        0

    )

    return size <= max_size


"""
==================================
CREATE UPLOAD FOLDERS
==================================
"""

def create_upload_folders(

    base_folder

):

    folders = [

        "covers",

        "banners",

        "chapters"

    ]

    for folder in folders:

        os.makedirs(

            os.path.join(

                base_folder,

                folder

            ),

            exist_ok=True

        )
        
        """
==================================
DELETE FILE
==================================
"""

def delete_file(

    file_path

):

    if os.path.exists(

        file_path

    ):

        os.remove(

            file_path

        )

        return True

    return False


"""
==================================
FILE INFORMATION
==================================
"""

def file_info(

    file_path

):

    if not os.path.exists(

        file_path

    ):

        return None

    return {

        "filename": os.path.basename(

            file_path

        ),

        "size": os.path.getsize(

            file_path

        ),

        "extension": os.path.splitext(

            file_path

        )[1].lower()

    }


"""
==================================
FILE EXISTS
==================================
"""

def file_exists(

    file_path

):

    return os.path.exists(

        file_path

    )