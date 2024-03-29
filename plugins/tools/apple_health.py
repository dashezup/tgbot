import os
import csv
from io import StringIO, BytesIO
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from pyrogram import Client, filters, emoji
from pyrogram.types import Message

MAX_ZIP_FILE_SIZE = 10485760


@Client.on_message(filters.document
                   & filters.incoming
                   & filters.regex(r"#apple_health$"))
async def command_apple_health(_, m: Message):
    doc = m.document
    valid_file = (
        m.caption == "#apple_health"
        and doc.file_size <= MAX_ZIP_FILE_SIZE
        and doc.file_name == "export.zip"
        and doc.mime_type == "application/zip"
    )
    if not valid_file:
        return
    await m.reply_chat_action("typing")
    zip_file_path = await m.download()
    if zip_file_path is None:
        return
    with ZipFile(zip_file_path) as z:
        with z.open("apple_health_export/export.xml", "r") as f:
            xml_tree = ET.parse(f)
    os.remove(zip_file_path)
    xml_root = xml_tree.getroot()
    records = [
        (x.get('startDate', '')[:19], float(x.get('value', 0)), x.get('unit'))
        for x in xml_root.findall('Record')
        if x.get('type') == "HKQuantityTypeIdentifierBodyMass"
    ]
    if not records:
        return
    sio = StringIO()
    writer = csv.writer(sio, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    writer.writerows(records)
    bio = BytesIO(sio.getvalue().encode("utf-8"))
    bio.name = "apple-health-weight-{}-{}.csv".format(
        records[0][0][:10].replace('-', ''),
        records[-1][0][:10].replace('-', '')
    )
    caption = (
        "{} **Apple Health - Body Measurements - Weight** ({} records)\n"
        + "`< {} ({} {})`\n"
        + "`> {} ({} {})`"
    ).format(
        emoji.MOBILE_PHONE_WITH_ARROW,
        len(records),
        records[0][0][:10],
        records[0][1],
        records[0][2],
        records[-1][0][:10],
        records[-1][1],
        records[-1][2],
    )
    await m.reply_chat_action("upload_document")
    await m.reply_document(bio, caption=caption, quote=True)
