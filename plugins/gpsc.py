import requests
import json
from pyrogram import Client, filters
from pyrogram.types import Message
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode

@Client.on_message(filters.command(["gpsc"]))
async def gpsc_login(bot: Client, m: Message):
    global cancel
    cancel = False
    editable = await m.reply_text("Send your **Mobile Number** to receive OTP.")
    
    # Step 1: Send mobile number to receive OTP
    input1: Message = await bot.listen(editable.chat.id)
    mobile_number = input1.text
    await input1.delete(True)
    
    # API endpoint to send OTP
    otp_url = "https://gpscvideoapi.example.com/send_otp"  # Replace with actual API endpoint
    payload = {"mobile_number": mobile_number}
    
    scraper = cloudscraper.create_scraper()
    otp_response = scraper.post(otp_url, data=payload).json()
    
    if otp_response.get("status") == "success":
        await editable.edit("OTP sent to your mobile number. Please enter the OTP.")
        
        # Step 2: Receive OTP from user
        input2: Message = await bot.listen(editable.chat.id)
        otp = input2.text
        await input2.delete(True)
        
        # API endpoint to verify OTP and login
        login_url = "https://gpscvideoapi.example.com/verify_otp"  # Replace with actual API endpoint
        login_payload = {"mobile_number": mobile_number, "otp": otp}
        
        login_response = scraper.post(login_url, data=login_payload).json()
        
        if login_response.get("status") == "success":
            userid = login_response["data"]["userid"]
            token = login_response["data"]["token"]
            
            await editable.edit("**Login Successful**")
            
            # Fetch user's courses
            hdr1 = {
                "Host": "gpscvideoapi.example.com",
                "Client-Service": "Appx",
                "Auth-Key": "appxapi",
                "User-Id": userid,
                "Authorization": token
            }
            
            course_url = "https://gpscvideoapi.example.com/get/mycourse?userid=" + userid
            res1 = requests.get(course_url, headers=hdr1)
            b_data = res1.json()['data']
            
            cool = ""
            for data in b_data:
                t_name = data['course_name']
                FFF = "**BATCH-ID - BATCH NAME - INSTRUCTOR**"
                aa = f" ```{data['id']}```      - **{data['course_name']}**\n\n"
                if len(f'{cool}{aa}') > 4096:
                    cool = ""
                cool += aa
            
            await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
            
            editable1 = await m.reply_text("**Now send the Batch ID to Download**")
            input2 = await bot.listen(editable.chat.id)
            raw_text2 = input2.text
            
            # Fetch subjects for the selected batch
            subject_url = "https://gpscvideoapi.example.com/get/allsubjectfrmlivecourseclass?courseid=" + raw_text2
            html = scraper.get(subject_url, headers=hdr1).content
            output0 = json.loads(html)
            subjID = output0["data"]
            
            await m.reply_text(subjID)
            
            editable1 = await m.reply_text("**Enter the Subject Id shown in the above response**")
            input3 = await bot.listen(editable.chat.id)
            raw_text3 = input3.text
            
            # Fetch topics for the selected subject
            topic_url = "https://gpscvideoapi.example.com/get/alltopicfrmlivecourseclass?courseid=" + raw_text2 + "&subjectid=" + raw_text3
            res3 = requests.get(topic_url, headers=hdr1)
            b_data2 = res3.json()['data']
            
            vj = ""
            for data in b_data2:
                tids = data["topicid"]
                idid = f"{tids}&"
                if len(f"{vj}{idid}") > 4096:
                    vj = ""
                vj += idid
            
            vp = ""
            for data in b_data2:
                tn = data["topic_name"]
                tns = f"{tn}&"
                if len(f"{vp}{tn}") > 4096:
                    vp = ""
                vp += tns
            
            cool1 = ""
            for data in b_data2:
                t_name = data["topic_name"]
                tid = data["topicid"]
                zz = len(tid)
                BBB = f"{'**TOPIC-ID    - TOPIC     - VIDEOS**'}\n"
                hh = f"```{tid}```     - **{t_name} - ({zz})**\n"
                if len(f'{cool1}{hh}') > 4096:
                    cool1 = ""
                cool1 += hh
            
            await m.reply_text(f'Batch details of **{t_name}** are:\n\n{BBB}\n\n{cool1}')
            
            editable = await m.reply_text(f"Now send the **Topic IDs** to Download\n\nSend like this **1&2&3&4** so on\nor copy paste or edit **below ids** according to you :\n\n**Enter this to download full batch :-**\n```{vj}```")
            input4 = await bot.listen(editable.chat.id)
            raw_text4 = input4.text
            
            editable3 = await m.reply_text("**Now send the Resolution**")
            input5 = await bot.listen(editable.chat.id)
            raw_text5 = input5.text
            
            try:
                xv = raw_text4.split('&')
                for y in range(0, len(xv)):
                    t = xv[y]
                    
                    hdr11 = {
                        "Host": "gpscvideoapi.example.com",
                        "Client-Service": "Appx",
                        "Auth-Key": "appxapi",
                        "User-Id": userid,
                        "Authorization": token
                    }
                    
                    res4 = requests.get("https://gpscvideoapi.example.com/get/livecourseclassbycoursesubtopconceptapiv3?topicid=" + t + "&start=-1&courseid=" + raw_text2 + "&subjectid=" + raw_text3, headers=hdr11).json()
                    
                    topicid = res4["data"]
                    vj = ""
                    for data in topicid:
                        tids = data["Title"]
                        idid = f"{tids}"
                        if len(f"{vj}{idid}") > 4096:
                            vj = ""
                        vj += idid
                    
                    vp = ""
                    for data in topicid:
                        tn = data["download_link"]
                        tns = f"{tn}"
                        if len(f"{vp}{tn}") > 4096:
                            vp = ""
                        vp += tn
                    
                    vs = ""
                    for data in topicid:
                        tn0 = data["pdf_link"]
                        tns0 = f"{tn0}"
                        if len(f"{vs}{tn0}") > 4096:
                            vs = ""
                        vs += tn0
                    
                    cool2 = ""
                    for data in topicid:
                        if data["download_link"]:
                            b64 = data["download_link"]
                        else:
                            b64 = data["pdf_link"]
                        tid = data["Title"]
                        zz = len(tid)
                        key = "638udh3829162018".encode("utf8")
                        iv = "fedcba9876543210".encode("utf8")
                        ciphertext = bytearray.fromhex(b64decode(b64.encode()).hex())
                        cipher = AES.new(key, AES.MODE_CBC, iv)
                        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
                        b = plaintext.decode('utf-8')
                        cc0 = f"{tid}:{b}"
                        if len(f'{cool2}{cc0}') > 4096:
                            cool2 = ""
                        cool2 += cc0
                        mm = "GPSCVideo"
                        with open(f'{mm}.txt', 'a') as f:
                            f.write(f"{tid}:{b}\n")
                
                await m.reply_document(f"{mm}.txt")
            except Exception as e:
                await m.reply_text(str(e))
            await m.reply_text("Done")
        else:
            await editable.edit("**Login Failed. Please try again.**")
    else:
        await editable.edit("**Failed to send OTP. Please try again.**")
