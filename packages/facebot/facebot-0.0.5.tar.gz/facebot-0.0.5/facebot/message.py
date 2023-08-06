# -*- encoding: utf-8 -*-
import logging
from urllib import urlencode
import re
import time

import requests

log = logging.getLogger('facebook')
log.setLevel(logging.WARN)

message_url = 'https://www.facebook.com/ajax/mercury/send_messages.php'
upload_url = 'https://upload.facebook.com/ajax/mercury/upload.php?'


def send_group(fb, thread, body, pic=None):
    data = {
        "message_batch[0][action_type]": "ma-type:user-generated-message",
        "message_batch[0][author]": "fbid:%s" % (fb.user_id),
        "message_batch[0][source]": "source:chat:web",
        "message_batch[0][body]": body,
        "message_batch[0][signatureID]": "3c132b09",
        "message_batch[0][ui_push_phase]": "V3",
        "message_batch[0][status]": "0",
        "message_batch[0][thread_fbid]": thread,
        "client": "mercury",
        "__user": fb.user_id,
        "__a": "1",
        "__dyn": "7n8anEBQ9FoBUSt2u6aAix97xN6yUgByV9GiyFqzQC-C26m6oDAyoSnx2ubhHAyXBBzEy5E",
        "__req": "c",
        "fb_dtsg": fb.dtsg,
        "ttstamp": "26581691011017411284781047297",
        "__rev": "1436610",
    }

    if pic:
        # upload the picture and get picture form data
        new_data = upload_picture(fb, pic)
        if new_data:
            # merge together to send message with picture
            data.update(new_data)

    fb.session.post(message_url, data)


def send_person(fb, person, body, pic=None):
    data = {
        "message_batch[0][action_type]": "ma-type:user-generated-message",
        "message_batch[0][author]": "fbid:%s" % (fb.user_id),
        "message_batch[0][source]": "source:chat:web",
        "message_batch[0][body]": body,
        "message_batch[0][signatureID]": "3c132b09",
        "message_batch[0][ui_push_phase]": "V3",
        "message_batch[0][status]": "0",
        "message_batch[0][specific_to_list][0]": "fbid:%s" % (person),
        "message_batch[0][specific_to_list][1]": "fbid:%s" % (fb.user_id),
        "client": "mercury",
        "__user": fb.user_id,
        "__a": "1",
        "__dyn": "7n8anEBQ9FoBUSt2u6aAix97xN6yUgByV9GiyFqzQC-C26m6oDAyoSnx2ubhHAyXBBzEy5E",
        "__req": "c",
        "fb_dtsg": fb.dtsg,
        "ttstamp": "26581691011017411284781047297",
        "__rev": "1436610",
    }

    if pic:
        # upload the picture and get picture form data
        new_data = upload_picture(fb, pic)
        if new_data:
            # merge together to send message with picture
            data.update(new_data)

    fb.session.post(message_url, data)


def upload_picture(fb, pic):
    params = {
        "__user": fb.user_id,
        "__a": "1",
        "__dyn": "7n8anEBQ9FoBUSt2u6aAix97xN6yUgByV9GiyFqzQC-C26m6oDAyoSnx2ubhHAyXBBzEy5E",
        "__req": "c",
        "fb_dtsg": fb.dtsg,
        "ttstamp": "26581691011017411284781047297",
        "__rev": "1436610",
        'ft[tn]': '+M',
    }
    # upload the image to facebook server, filename should be unique
    res = fb.session.post(upload_url + urlencode(params), files={
        'images_only': 'true',
        'upload_1024': (str(time.time()), requests.get(pic).content, 'image/jpeg')
    })

    # check status code
    if res.status_code != 200:
        return

    # check image_id is valid
    m = re.search(r'"image_id":(\d+),', res.content)
    if not m:
        return

    image_id = m.group(1)
    return {
        "message_batch[0][has_attachment]": "true",
        "message_batch[0][preview_attachments][0][upload_id]": "upload_1024",
        "message_batch[0][preview_attachments][0][attach_type]": "photo",
        "message_batch[0][preview_attachments][0][preview_uploading]": "true",
        "message_batch[0][preview_attachments][0][preview_width]": "540",
        "message_batch[0][preview_attachments][0][preview_height]": "720",
        "message_batch[0][image_ids][0]": image_id,
    }
