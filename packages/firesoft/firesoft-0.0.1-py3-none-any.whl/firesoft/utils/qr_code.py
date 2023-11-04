def generate_background_qrcode(
        data: str,
        background_path: str,
        error_correction: str = None,
        version: int = None,
        target_path: str = None,
        target_stream=None,
        scale: int = None,
        dark_color: str = None,
        data_dark_color: str = None,
        data_light_color: str = None,
        border_thickness: int = None,
        kind: str = None,
):
    assert target_path or target_stream, 'Either target_path or target_stream must be provided'
    assert not (target_path and target_stream), 'Either target_path or target_stream must be provided, not both'
    assert kind or target_path, 'kind must be provided if target_path is not provided'
    assert kind in [None, 'png', 'jpg'], 'kind must be None, png or jpg'
    assert error_correction in [None, 'l', 'm', 'q', 'h'], 'error_correction must be None, l, m, q or h'
    assert version is None or version in range(1, 41), 'version must be None or in 1-40 range'

    import segno
    qrcode = segno.make(data, error=error_correction, version=version)

    if target_path:
        qrcode.to_artistic(
            scale=scale,
            dark=dark_color,
            data_dark=data_dark_color,
            data_light=data_light_color,
            border=border_thickness,
            background=background_path,
            target=target_path,
        )
    else:
        qrcode.to_artistic(
            scale=scale,
            dark=dark_color,
            data_dark=data_dark_color,
            data_light=data_light_color,
            border=border_thickness,
            background=background_path,
            target=target_stream,
            kind=kind,
        )


def generate_artistic_qr_codes_pdf_from_excel(
        qr_bg_image_path: str,
        pdf_file_path: str,
        excel_file_path: str,
        excel_column_name: str,
        images_per_row: int = 3,
        with_labels: bool = False,
        error_correction: str = 'h',
        qr_version: int = 7,
        scale: int = 4,
        dark_color: str = 'darkred',
        data_dark_color: str = 'black',
        data_light_color: str = 'white',
        border_thickness: int = 3,
        kind: str = 'png',
):
    from firesoft.utils.files import read_values_from_excel_column
    qr_codes_data_list = read_values_from_excel_column(excel_file_path, excel_column_name)
    if isinstance(qr_codes_data_list, str):
        return qr_codes_data_list

    qr_images_list = []

    from io import BytesIO
    out = BytesIO()
    for data in qr_codes_data_list:
        generate_background_qrcode(
            data=data,
            background_path=qr_bg_image_path,
            target_stream=out,
            scale=scale,
            dark_color=dark_color,
            data_dark_color=data_dark_color,
            data_light_color=data_light_color,
            border_thickness=border_thickness,
            version=qr_version,
            error_correction=error_correction,
            kind=kind,
        )

        qr_images_list.append(out)

    from firesoft.utils.files import generate_images_pdf
    generate_images_pdf(
        images_list=qr_images_list,
        images_labels_list=qr_codes_data_list if with_labels else None,
        pdf_file_path=pdf_file_path,
        images_per_row=images_per_row,
    )

    return None


def generate_artistic_qr_codes_pdf_from_list(
        qr_codes_data_list: list,
        qr_bg_image_path: str,
        pdf_file_path: str,
        images_per_row: int = 3,
        with_labels: bool = False,
        error_correction: str = 'h',
        qr_version: int = 7,
        scale: int = 4,
        dark_color: str = 'darkred',
        data_dark_color: str = 'black',
        data_light_color: str = 'white',
        border_thickness: int = 3,
        kind: str = 'png',
):
    qr_images_list = []

    from io import BytesIO
    out = BytesIO()
    for data in qr_codes_data_list:
        generate_background_qrcode(
            data=data,
            background_path=qr_bg_image_path,
            target_stream=out,
            scale=scale,
            dark_color=dark_color,
            data_dark_color=data_dark_color,
            data_light_color=data_light_color,
            border_thickness=border_thickness,
            version=qr_version,
            error_correction=error_correction,
            kind=kind,
        )

        qr_images_list.append(out)

    from firesoft.utils.files import generate_images_pdf
    generate_images_pdf(
        images_list=qr_images_list,
        images_labels_list=qr_codes_data_list if with_labels else None,
        pdf_file_path=pdf_file_path,
        images_per_row=images_per_row,
    )
