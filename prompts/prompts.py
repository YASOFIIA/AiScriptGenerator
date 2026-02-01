from __future__ import annotations

from app.utils.csv_parser import CsvRow


# Prompt 1 (Perplexity)
def build_prompt_1(row: CsvRow) -> str:
    return (
        "Please provide an extensive briefing on the following topic that I wish to create a social media episode for.\n"
        "I only want this research to be done on the topic, no other similar topics or situations. "
        "\"Episode Code -\n"
        "Number - Series Name - Episode Topic\" Format:\n"
        "INPUT FROM CSV FILE:\n"
        f"{row.raw_text}\n\n"
        "Please all be sure to list the \"Episode Code - Number - Series Name - Episode Topic\" at the top as a\n"
        "heading. Example: \"26J13-2 - Things that frustrated so many Pokemon players!\""
    )

# Prompt 2 (Gemini)
def build_prompt_2(perplexity_output: str) -> str:
    return (
        "The following information is crucial for you to understand for the task. Please memorize this briefing that\n"
        "my assistant provided for me, you will use this information for the task I'm about to give you:\n"
        f"{perplexity_output}"
    )

# Prompt 3 (Gemini)
def build_prompt_3(memorized_briefing: str, episode_code: str) -> str:
    return (
        "\"I want you to write a short-form video social media script that is optimized for viewer retention (so our\n"
        "main goal is for viewers to stick around to the end of the video, because that will maximize the views for\n"
        "the video, so the video needs to be fast paced). I created a special framework to help you with this\n"
        "This is my framework for writing social media scripts:\n"
        "Title: Simply stating the name of the *video series*\n"
        "Background information: Giving information that’s necessary for the video to have.\n"
        "Re-hook: Adding some sort of anticipation / curiosity-arousing / emotion anytime the viewer may start to\n"
        "get bored in order to keep the script exciting, usually starting with the word “But.”\n"
        "I repeat these 2 steps mentioned above until it’s time to finish the script.\n"
        "A few more important things to note about my writing style is:\n"
        "1. I say everything in chronological order, and never spoil the point of the video until the very end. (THIS\n"
        "IS VERY IMPORTANT!)\n"
        "2. I always use a conversational writing style and be sure to use SIMPLE vocabulary that a 14 year old\n"
        "could understand.\n"
        "3. I usually start by saying *back in (insert date) … (event happened)\n"
        "4. I stay LASER-FOCUSED on the topic at hand because going off-topic will make the video longer than it\n"
        "needs to be and will cause the viewer to scroll away prematurely.\n"
        "5. I use proper punctuation.\n"
        "6. If the number is over 999, I write out numbers instead of using their numeric symbols. The ONLY\n"
        "exception to this is if I'm talking about the year. (Ex: Normal number: “One-thousand five hundred twelve.\"\n"
        "Year: \"2022.”)\n"
        "7. EXTREMELY IMPORTANT: I SAVE THE MOST IMPORTANT PART OF THE SCRIPT (THE REASON\n"
        "THE VIEWER IS WATCHING / WHAT THEY’RE WAITING FOR) UNTIL THE END\n"
        "8. Make sure the re-hooks are well thought out and curiosity invoking - (Ex: “But little did anyone know at\n"
        "the time they had a secret trick up their sleeve.” “But there was actually a huge reason behind why this\n"
        "happened,” “but that's still just the beginning of his story.” “but sadly, this story doesn't have a happy\n"
        "ending.” etc.\n"
        "Here’s an example of a script that’s exactly how I want my scripts written based on the framework I\n"
        "provided above - this was written for my “25L21-1 - Players who became the best after changing\n"
        "positions!” series:\n"
        "[Title / Series Name]\n"
        "25L1-1 - Clubs who betrayed their own players!\n"
        "[Context]\n"
        "Back in 2014, Real Madrid signed Keylor Navas after he impressed at the World Cup with Costa Rica. He\n"
        "was supposed to be their backup goalkeeper, but when Iker Casillas left in 2015, Navas became the new\n"
        "number one. And he didn't disappoint, leading Real Madrid to one of the most dominant eras in club\n"
        "history.\n"
        "[Re-hook]\n"
        "But there was one big problem. Real Madrid never really wanted him.\n"
        "You see, just months after making him their starter, they tried to replace him with David De Gea in a\n"
        "deadline day swap deal. But thanks to a fax machine error, the transfer collapsed and Navas stayed.\n"
        "Now, Navas could have felt upset and whined about this, but instead of complaining, he stepped up,\n"
        "helping Madrid win three straight Champions League titles from 2016 to 2018. He was a wall in goal,\n"
        "making crucial saves in every final.\n"
        "[Re-hook]\n"
        "But apparently, Real Madrid didn't care.\n"
        "Because in 2018, they signed Thibaut Courtois from Chelsea and immediately benched Navas. He went\n"
        "from being the hero of three Champions League wins to being completely sidelined. Even when Courtois\n"
        "struggled, Navas barely got a chance.\n"
        "[Re-hook]\n"
        "But what happened next was just cold.\n"
        "What I mean is that in 2019, Real Madrid pushed him out completely, selling him to PSG. After everything\n"
        "he'd done, they didn't even give him a proper farewell and just like that, one of Madrid's greatest\n"
        "goalkeepers was gone.\n"
        "[End of script]\n"
        "Please create a 200+ word script for my series that has the number 1 goal of viewer retention based on\n"
        "the information that you have just been fed and 1. please use my social media writing framework, 2. use\n"
        "the bracket descriptors to describe each part of the script, like background information, re-hook, end of\n"
        "script, etc. 3. Only include RELEVANT/NECCESSARY information so the script doesn’t get too long (it’s\n"
        "fine if it’s a long story that needs many details, but for stories that don’t need that level of detail don’t go\n"
        "crazy with the details) 4. MAKE SURE ITS FAST PACED 5. Be specific when talking about this, so be\n"
        "sure to use numbers, important details instead of just paraphrasing. 6. DO NOT EXCEED 300 WORDS\n"
        "UNLESS THE SCRIPT ABSOLUTELY REQUIRES IT. 7. Do not use any 'm dashes'\n\n"
        "-----\n"
        f"EPISODE CODE: {episode_code}\n"
        "BRIEFING TO USE (memorize + use as facts for the script):\n"
        f"{memorized_briefing}"
    )

# Prompt 4 (Gemini)
def build_prompt_4(script_with_brackets: str) -> str:
    return (
        "Great. Now combine a bunch of these small sentences that you used into larger sentences. Make sure\n"
        "not to use any 'm dashes' (—).\n\n"
        f"{script_with_brackets}"
    )

# Prompt 5 (Gemini)
def build_prompt_5(script_combined_sentences: str) -> str:
    return (
        "Great, now I want you to do the following:\n"
        "If the script you just sent is over 315 words (not including bracket descriptors), please scan the text to see\n"
        "if there's any pieces that are \"additional information\" that the script really doesn't require and remove it.\n"
        "If the script you just sent is less than 300 words (not including bracket descriptors), keep it the same exact\n"
        "way. As always make sure not to use any 'm dashses' (—)\n\n"
        f"{script_combined_sentences}"
    )

# Prompt 6 (Gemini)
def build_prompt_6(script_trimmed: str) -> str:
    return (
        "Great, now can you scan this text to see if the word 'but' is used in back to back sentences? If yes, reword\n"
        "the first 'but' into different phrasing so the script doesn't sound awkward with a double-but - if no, do\n"
        "nothing. As always make sure not to use any 'm dashses' (—)\n\n"
        f"{script_trimmed}"
    )

# Prompt 7 (Gemini)
def build_prompt_7(script_no_double_but: str) -> str:
    return (
        "remove bracket descriptors\n\n"
        f"{script_no_double_but}"
    )

# Prompt 8 (Gemini)
def build_prompt_8(script_no_brackets: str, episode_code: str) -> str:
    return (
        "\"Finally check to see if the title matches the story well, especially how it ends. If yes, do nothing. If not,\n"
        "change it so it's something that matches the script, so it's not clickbaity. Make sure it's engaging so it's\n"
        "going to grab people's attention / curiosity in a way that makes them stick around to get the final bit of\n"
        "information in the video and make sure it's plural. Examples of titles:\n"
        "* People who could have been incredibly rich BUT instead chose to make the world a better place.\n"
        "* Teams that got caught cheating!\n"
        "* Plays that were so dirty that they ruined careers!\n"
        "* Players who sued their own team!\n"
        "* Teams that were awful but then became insane.\n"
        "* Players who had incredible starts to their careers but then became awful!\n"
        "Be sure to keep the episode code in the beginning as well. And then put in Parenthesis right next to it,\n"
        "what the original title was before you changed it. Last but not least, keep the title rather vague as opposed\n"
        "to specific and use simple words that are easy for people to understand. And be sure to use the topic in\n"
        "the title, ex: Baseball, Soccer, Pokemon, Naruto, etc.\"\n"
        "Display the entire script and don't say any other words so I can easily copy and paste it into a word\n"
        "document.\n\n"
        f"(Episode code reference: {episode_code})\n\n"
        f"{script_no_brackets}"
    )

# Prompt 9 (Perplexity)
def build_prompt_9(final_script_from_gemini: str) -> str:
    return (
        "Please break down this final script sentence by sentence and verify that there is no misinformation. Be\n"
        "sure to label each statement as correct / partially incorrect / incorrect and use emojis. Be sure to cite your\n"
        "sources. Please format this by giving a statement at the top of your output saying: Correct sentences: X,\n"
        "Incorrect sentences: X, Partially incorrect sentences: X, and the proceeding to give the fact\n"
        "check-information.\n\n"
        f"{final_script_from_gemini}"
    )

# Prompt 10 (Perplexity)
def build_prompt_10(fact_check_output: str, final_script_from_gemini: str) -> str:
    return (
        "Based on the fact check you just conducted, I want you to do the following:\n"
        "If there's any major inaccurate information, do the following: \"write MAJOR ERRORS DETECTED:\" then\n"
        "make the following changes to the script - keep the script almost exactly the same as I pasted it in, except\n"
        "change the major inaccurate statements so they are accurate, and make sure to write them in italics so I\n"
        "can easily identify them. As always make sure not to use any 'm dashses' (—)\n"
        "If there's no major inaccurate information, don't change anything, just say: \"NO MAJOR ERRORS:\" then\n"
        "display the script exactly how I pasted it in.\n\n"
        "-----\n"
        "FACT CHECK YOU JUST DID:\n"
        f"{fact_check_output}\n\n"
        "-----\n"
        "SCRIPT TO OUTPUT (exactly, unless major errors):\n"
        f"{final_script_from_gemini}"
    )
