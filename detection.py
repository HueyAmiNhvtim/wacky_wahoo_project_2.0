from textblob import TextBlob
import regex
import json

# I don't have time to refractor the thing. Sorry!
# Differentiate characters from emoji
# If the string does not contain a single hiragana character after going through regex
# check, immediately flag it as emoji spam

# Thanks mgaitan for this emoji unicode list.

# BUG: There is a bug here in which a hell lotta JP chars are counted as being in "other" category. check the emoji pattern or sth
EMOJI_PATTERN = regex.compile(
    "^["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251" 
    "]+$")

# It should work with Japanese and Chinese characters (such as hiragana, katakana, kanji, Cantonese)
emote_spam_pattern = r"^(:_?\w+_?:)+$"
exceptions_list = [ # From 2024 Huy: lmao.........................
    r"^(big)?\s?kusa$", r"^kekw$", r"^pepega$", r"^monkas$",
    r"^l((ol)|(ul))+$", r"^guh$", r"^hic$", r"^poggers?$"
    r"^gomenasorry$", r"^ara ara$", r"^yamete\skudastop$",
    r"^pogchamp$", r"birb", r"^(good)?by(e)+", r"^(ba+i*)+$", r"^(pain)?/s?peko$", r"^10q$",
    r"^yab(ai)?", r"^subaramazing$", r"^(po)?lma(o)+$", r"^lewds?$", r"rip(!)*", r"^y(e)*t$",
    r"^bottom left$", r"^gg$", r"^hey moona$"
                   ]

streamers_list = ["kiara"]
filepath = "streamer_comments/amelia/live/amelia_LC_#0.json"


def load_file_path(streamer):
    live_file_path = f"streamer_comments/{streamer}/live"
    post_live_file_path = f"streamer_comments/{streamer}/post_live"
    vid_info = f"streamer_comments/{streamer}/vid_info"
    for i in range(30):
        file_to_load = f"streamer_comments/{streamer}/full_data"
        lc_dict = live_lang_analysis(streamer, live_file_path, i)
        nlc_dict = unlive_lang_analysis(streamer, post_live_file_path, i)
        vid_details = vid_info_extraction(streamer, vid_info, i)
        vid_details["live_chat_lang_distributions"] = lc_dict
        vid_details["comment_sections_lang_distributions"] = nlc_dict
        file_to_load += f"/{streamer}'s_stream_#{i}_full_data.json"
        with open(file_to_load, mode="w") as f:
            json.dump(vid_details, f)
        print(f"-----------Finish {streamer.title()}'s video #{i}-----------")


def live_lang_analysis(streamer, file_path, index):
    """This is for the first file"""
    file_path = file_path + f"/{streamer}_LC_#{index}.json"
    lang_composition = {"length": 0,
                        "num_extracted_comments": 0,
                        "emote_spam": 0,
                        "other": 0,
                        "en": 0,
                        "ja": 0}
    with open(file_path, mode="r") as f:
        live_chat_list = json.load(f)
        lang_composition["num_extracted_comments"] = len(live_chat_list)
        for key, value in live_chat_list[-1].items():
            lang_composition["length"] = value
    for comment in live_chat_list:
        # From 2024 Huy: wtf did the below mean???
        en_num_before = lang_composition["en"]
        for key in comment.keys():
            # Lowercase all the comments so that I don't have to put in more exceptions in the
            # goddamn exceptions list.
            actual_comment = key.lower()
        for exception in exceptions_list:
            if regex.match(exception, actual_comment):
                lang_composition["en"] += 1
                break
        en_num_now = lang_composition["en"]
        # Check so that there is no overlapping
        if en_num_now != en_num_before:
            # Break out of the loop
            continue
        else:
            if regex.match(emote_spam_pattern, actual_comment) or regex.match(EMOJI_PATTERN, actual_comment):
                lang_composition["emote_spam"] += 1
            else:
                lang_code = TextBlob(actual_comment).detect_language()
                # lang_code = cld3.get_language(actual_comment)[0]
                if lang_code == "ja":
                    lang_composition["ja"] += 1
                elif lang_code == "en":
                    lang_composition["en"] += 1
                else:
                    lang_composition["other"] += 1
    print(f"Length of {streamer}'s video #{index + 1}: {lang_composition['length']} seconds")
    return lang_composition


def unlive_lang_analysis(streamer, file_path, index):
    """For the comment section"""
    file_path = file_path + f"/{streamer}_post_stream_#{index}.json"
    lang_composition = {"num_extracted_comments": 0,
                        "emote_spam": 0,
                        "other": 0,
                        "en": 0,
                        "ja": 0}
    with open(file_path, mode="r") as f:
        unlive_chat_list = json.load(f)
        lang_composition["num_extracted_comments"] = len(unlive_chat_list)
    for comment in unlive_chat_list:
        en_num_before = lang_composition["en"]
        actual_comment = comment.lower()
        for exception in exceptions_list:
            if regex.match(exception, actual_comment):
                lang_composition["en"] += 1
                break
        en_num_now = lang_composition["en"]
        # Check so that there is no overlapping
        if en_num_now != en_num_before:
            # Move onto the next comment immediately
            continue
        else:
            if actual_comment == "":
                # Yeah, I can't extract the emoji out of the comment.
                lang_composition["emote_spam"] += 1
            else:
                # lang_code = cld3.get_language(actual_comment)[0]
                lang_code = TextBlob(actual_comment).detect_language()
                if lang_code == "ja" or lang_code == "en":
                    lang_composition[lang_code] += 1
                else:
                    lang_composition["other"] += 1
    return lang_composition


def vid_info_extraction(streamer, file_path, index):
    file_path = file_path + f"/{streamer}_stream_#{index}.json"
    # Extract number out of the viewcount and total comments
    PATTERN = r"^(\d{1,3},)*,?\d{1,3}"
    with open(file_path, mode="r") as f:
        vid_list = json.load(f)
        total_views = regex.match(PATTERN, vid_list[2]).group(0)
        # Remove the , out of the number such as 800,000 for proper conversion into int.
        total_views = int(regex.sub(",", "", total_views))
        recorded_comments = regex.match(PATTERN, vid_list[3]).group(0)
        recorded_comments = int(regex.sub(",", "", recorded_comments))
        vid_info_dict = {
            'name': vid_list[1],
            'views': total_views,
            "num_comments": recorded_comments
        }
    return vid_info_dict


def interval_stuff(streamer):
    """Divide the stream into 10 equal parts, each part record the lang distributions"""
    # 30 streams per streamer. Here ya go
    for i in range(30):
        lc_file_path = f"streamer_comments/{streamer}/live/{streamer}_LC_#{i}.json"
        interval_analysis(streamer, lc_file_path, i)
        print(f"-----------Finish {streamer.title()}'s video #{i}-----------")


def interval_analysis(streamer, lc_file_path, vid_no):
    """Not gonna lie, I don't want to read my garbage code right now."""
    vid_info = {}
    index = 0
    message_list = []
    time_stamp_list = []
    # 10 equal parts per stream
    for i in range(10):
        vid_info[i] = []
    with open(lc_file_path, mode="r") as f:
        livechat_comments = json.load(f)
    for i in livechat_comments:
        for key, value in i.items():
            message_list.append(key)
            time_stamp_list.append(value)

    last_mesg_time = time_stamp_list[-1]
    parts_length = last_mesg_time / 10
    start_interval = 0
    end_interval = parts_length
    while index <= 9 and end_interval <= last_mesg_time:
        if end_interval < last_mesg_time:
            for i in range(len(time_stamp_list)):
                range_before_deletion = i
                time_stamp = time_stamp_list[i]
                if start_interval <= time_stamp < end_interval:
                    vid_info[index].append(message_list[i])
                else:
                    break
            # Speed up the damn thing instead of having to reloop it everytime.
            # Otherwise, it's gonna take forever.
            del time_stamp_list[:range_before_deletion]
            del message_list[:range_before_deletion]
        else:
            for i in range(len(time_stamp_list)):
                vid_info[index].append(message_list[i])
        start_interval = end_interval
        end_interval += parts_length
        end_interval = round(end_interval, 1)
        index += 1
    return load_intervals_for_lang_detection(streamer, vid_info, vid_no)


def load_intervals_for_lang_detection(streamer, vid_info: dict, index):
    for key, value in vid_info.items():
        interval_composition = lang_detection_interval(value)
        vid_info[key] = interval_composition
    file_path = f"streamer_comments/{streamer}/lang_dis_intervals/{streamer}_stream_#{index}_intervals_lang_distribution.json"
    with open(file_path, mode="w") as f:
        json.dump(vid_info, f)
    return vid_info


def lang_detection_interval(message_list: list):
    lang_composition = {"emote_spam": 0,
                        "other": 0,
                        "en": 0,
                        "ja": 0}
    for comment in message_list:
        en_num_before = lang_composition["en"]
        actual_comment = comment.lower()
        for exception in exceptions_list:
            if regex.match(exception, actual_comment):
                lang_composition["en"] += 1
                break
        en_num_now = lang_composition["en"]
        # Check so that there is no overlapping
        if en_num_now != en_num_before:
            # Break out of the loop => Prevent overlapping
            continue
        else:
            if regex.match(emote_spam_pattern, actual_comment) or regex.match(EMOJI_PATTERN, actual_comment):
                lang_composition["emote_spam"] += 1
            else:
                # lang_code = cld3.get_language(actual_comment)[0]
                lang_code = TextBlob(actual_comment).detect_language()
                if lang_code == "ja":
                    lang_composition["ja"] += 1
                elif lang_code == "en":
                    lang_composition["en"] += 1
                else:
                    lang_composition["other"] += 1
    return lang_composition


for vtuber in streamers_list:
    print(f"Starting analyzing {vtuber.title()}'s videos...")
    load_file_path(vtuber)
    #interval_stuff(vtuber)
    print(f"\n-----------FINISH {vtuber.upper()}'S VIDEOS-----------\n")


