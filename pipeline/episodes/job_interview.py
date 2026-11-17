"""Episode: AI for Your Job Interview in 2026.
Each scene: kind, number, title, beats. Each beat: say (narration), optional tts (pronunciation override),
optional card (name, description) or tip (text) that appears when the beat starts."""

CHANNEL = "AI for Every Job"
PRESENTER = "interviewee"
VOICE = "am_adam"
EPISODE = "AI for Your Job Interview in 2026"

# Tool sources (vendor pages, checked 2026-11-17):
# ChatGPT: https://chatgpt.com  ·  ChatGPT Voice: https://learn.chatgpt.com/training/walkthroughs/using-voice
#   and https://help.openai.com/en/articles/20001274-chatgpt-voice
# Claude: https://claude.com  ·  Claude voice mode (beta): https://support.claude.com/en/articles/11101966-use-voice-mode
# Microsoft Copilot mock interview coach:
#   https://learn.microsoft.com/en-in/training/modules/boost-productivity-with-copilot/4-elevate-your-job-search-with-copilot
# Gemini Live interview practice: https://grow.google/grow-your-career/articles/interview-tips/
#   (grow.google/interview-warmup now redirects here; Interview Warmup itself is deliberately not named)
# Yoodli interview roleplays and feedback: https://yoodli.ai/use-cases/interview-preparation

SCENES = [
    dict(kind="title", title="AI for Your Job Interview", year="2026",
         sub="One week out. The day before. The hour before. After.",
         beats=[
             dict(tts="You got the interview. Great news, and maybe a knot in your stomach. In 2026, A I can be a patient practice partner, if you use it honestly.",
                  say="You got the interview. Great news, and maybe a knot in your stomach. In 2026, AI can be a patient practice partner, if you use it honestly."),
             dict(say="So let's count down together: one week out, a few days out, the day before, the final hour, and the hours after the interview is over."),
             dict(say="And one line we will not cross. Everything here is preparation. No hidden help during the interview itself, no invented experience, and no secrets from your old employer."),
         ]),
    dict(kind="cards", num="01", title="One week out: the role",
         beats=[
             dict(say="One week out: understand the job. A job post is written for many readers. Work out what this team actually needs, and why they are hiring now."),
             # ChatGPT https://chatgpt.com · Claude https://claude.com
             dict(card=("Decode the job post", "Ask which problems this person will solve first"),
                  tts="Paste the job post into Chat G P T or Claude and ask: what problems will this person solve in their first three months, and which skills will they test most?",
                  say="Paste the job post into ChatGPT or Claude and ask: what problems will this person solve in their first three months, and which skills will they test most?"),
             dict(card=("Research the company", "Start from their own site, reports and announcements"),
                  say="Then research the company. Read its own website and recent announcements, paste a section in, and ask: explain this plainly, and what might it mean for this team?"),
             dict(card=("Check every fact", "Assistants mix up companies and repeat old news"),
                  say="An honest limit: assistants can mix up similar company names, or repeat old news. If a fact might come up in the interview, confirm it on an official page."),
         ]),
    dict(kind="cards", num="02", title="One week out: your stories",
         beats=[
             dict(say="Still one week out: your stories. Interviewers often say: tell me about a time when. The best answers are real moments, told clearly. Collect them now."),
             dict(card=("Get interviewed about you", "One question at a time, until you have ten real moments"),
                  say="Ask the assistant to interview you about your past jobs: ask me one question at a time about projects, conflicts and mistakes, until I have ten real moments."),
             dict(card=("Shape it with STAR", "Situation, task, action, result, from your facts only"),
                  tts="Pick one moment and shape it with S T A R: situation, task, action, result. Prompt: organise my notes into S T A R, keep my words, and add nothing I did not say.",
                  say="Pick one moment and shape it with STAR: situation, task, action, result. Prompt: organise my notes into STAR, keep my words, and add nothing I did not say."),
             dict(card=("Remove the secrets", "No client names, internal figures or code from old jobs"),
                  say="Before pasting anything, remove client names, internal figures, code, and anything your old employer would treat as confidential. Guarding secrets well shows good judgment, in the interview too."),
         ]),
    dict(kind="cards", num="03", title="Four days out: rehearse",
         beats=[
             dict(say="Four days out: practise out loud. A story that sounds fine in your head often comes out long and tangled. Saying it aloud a few times fixes that."),
             # ChatGPT Voice https://learn.chatgpt.com/training/walkthroughs/using-voice · Claude voice mode (beta) https://support.claude.com/en/articles/11101966-use-voice-mode
             dict(card=("Voice mode", "Spoken mock interviews in ChatGPT and Claude"),
                  tts="Chat G P T Voice, and Claude's voice mode in beta, let you talk instead of type. Try: you are the hiring manager for this role. Ask me six questions, one at a time.",
                  say="ChatGPT Voice, and Claude's voice mode in beta, let you talk instead of type. Try: you are the hiring manager for this role. Ask me six questions, one at a time."),
             # Copilot https://learn.microsoft.com/en-in/training/modules/boost-productivity-with-copilot/4-elevate-your-job-search-with-copilot
             # Gemini Live https://grow.google/grow-your-career/articles/interview-tips/
             dict(card=("Copilot  ·  Gemini Live", "Mock interviews with tips and feedback on your answers"),
                  say="Microsoft suggests asking Copilot for a mock interview with tips and feedback. Google suggests Gemini Live, in the Gemini mobile app, for a conversational interview with structured feedback."),
             # Yoodli https://yoodli.ai/use-cases/interview-preparation
             dict(card=("Yoodli", "Roleplays with follow-ups, then notes on pacing and fillers"),
                  tts="Yoodlee runs practice interviews as roleplays and asks follow up questions. Afterwards it points out filler words, pacing and unclear answers, the habits you rarely notice yourself.",
                  say="Yoodli runs practice interviews as roleplays and asks follow-up questions. Afterwards it points out filler words, pacing and unclear answers, the habits you rarely notice yourself."),
             dict(tip="Rehearse with AI. In the real interview, it stays switched off.",
                  tts="Rehearsal is where A I belongs. In the real interview, phone, video or online test, no hidden assistant and no script on screen. It is dishonest, and can end the process.",
                  say="Rehearsal is where AI belongs. In the real interview, phone, video or online test, no hidden assistant and no script on screen. It is dishonest, and can end the process."),
         ]),
    dict(kind="cards", num="04", title="Three days out: format",
         beats=[
             dict(say="Three days out: know your format. Phone screens, video calls, panels, and technical or case interviews each need different practice. Unsure which one it is? Ask the recruiter."),
             dict(card=("Phone and video", "A short opening; test camera, sound and light"),
                  say="For a phone screen, prepare a crisp opening about yourself. Ask the assistant: cut this to under two minutes spoken. For video, test your camera, sound and light beforehand."),
             dict(card=("Panel interviews", "Practise with several interviewers who want different things"),
                  say="For a panel, ask for a roleplay with three interviewers: a manager who wants results, a future teammate who values collaboration, and someone from finance asking about cost."),
             dict(card=("Technical and case", "Practice problems, with hints only when you ask"),
                  say="For technical or case interviews, ask for a practice problem at your level, and add: no answers. Let me think aloud, and hint only when I ask."),
         ]),
    dict(kind="cards", num="05", title="If you get a take-home",
         beats=[
             dict(tts="Some employers send a take-home task: a presentation, a writing sample, or a small coding or design exercise. Here, honesty about A I matters most, so slow down.",
                  say="Some employers send a take-home task: a presentation, a writing sample, or a small coding or design exercise. Here, honesty about AI matters most, so slow down."),
             dict(card=("Read the rules first", "Is AI allowed? If it is unclear, ask the recruiter"),
                  tts="First, look for any rule on A I in the instructions. If there is none, ask the recruiter politely: may candidates use A I tools here, and should I say how?",
                  say="First, look for any rule on AI in the instructions. If there is none, ask the recruiter politely: may candidates use AI tools here, and should I say how?"),
             dict(card=("Keep the thinking yours", "Your ideas, your structure, your final decisions"),
                  say="Even where it is allowed, the thinking must be yours. You may need to explain every choice in a later interview. If you cannot defend a line, cut it."),
             dict(card=("Say how you used it", "A short note on which tools helped, and with what"),
                  say="If you used an assistant, add a short honest note, like: I used it to check grammar and suggest test cases, and wrote the analysis myself. Openness builds trust."),
             dict(tip="Never use a past employer's documents, data or code in a task.",
                  tts="And never reuse a past employer's documents, data or code, with or without A I. It is not yours to share, and a careful employer will notice.",
                  say="And never reuse a past employer's documents, data or code, with or without AI. It is not yours to share, and a careful employer will notice."),
         ]),
    dict(kind="cards", num="06", title="Day before, hour before",
         beats=[
             dict(tts="The day before, most of the work is done. Now it is about good questions, calm logistics, and a clear head. A I helps a little, then steps aside.",
                  say="The day before, most of the work is done. Now it is about good questions, calm logistics, and a clear head. AI helps a little, then steps aside."),
             dict(card=("Questions to ask them", "About the team, the work, and what success looks like"),
                  say="Ask the assistant: based on this job post and my research, suggest ten questions to ask the interviewers. Keep the few you truly want answered, like how they judge success."),
             dict(card=("Know typical pay", "Research ranges from reputable sources, not a chatbot"),
                  say="If pay might come up, research typical ranges for the role from reputable sources, such as official surveys or published pay scales. Do not rely on a chatbot's guess."),
             dict(card=("The hour before: offline", "Read your own notes, breathe, close the apps"),
                  say="In the final hour, put the chatbot away. Read your one page of notes, written in your own words, check the address or link, and walk in as yourself."),
         ]),
    dict(kind="cards", num="07", title="After: thanks and review",
         beats=[
             dict(say="After the interview, while it is fresh, spend twenty minutes writing down what happened. Those notes become today's thank you message, and a better interview next time."),
             dict(card=("An honest thank-you", "Mention one real moment from the conversation"),
                  say="Give the assistant your notes and ask: draft a short thank you email mentioning our talk about onboarding. Then edit it until it sounds like you, and promise nothing new."),
             dict(card=("Review your answers", "Which answers landed, and which felt vague?"),
                  say="Then reflect. List the questions you were asked. Prompt: which answers sound strong, which were vague, and which extra story should I prepare next time?"),
             dict(card=("Learn from every outcome", "Thank them for a no, and ask for brief feedback"),
                  say="If the answer is no, reply graciously and ask for brief feedback. Not every employer will share it. Either way, add what you learned to your story bank."),
         ]),
    dict(kind="cards", num="★", title="Three rules",
         beats=[
             dict(tts="Finally, three simple rules for using A I around any interview. They protect your reputation, your former colleagues, and the trust of whoever ends up hiring you.",
                  say="Finally, three simple rules for using AI around any interview. They protect your reputation, your former colleagues, and the trust of whoever ends up hiring you."),
             dict(card=("1   Practise, never prompt", "AI before and after, never secretly during"),
                  tts="Rule one: practise with A I, but never be prompted by it. Use it before and after, never as hidden help while you are being interviewed or tested.",
                  say="Rule one: practise with AI, but never be prompted by it. Use it before and after, never as hidden help while you are being interviewed or tested."),
             dict(card=("2   Only true stories", "No invented skills, results or experience"),
                  tts="Rule two: tell only true stories. Never let A I invent skills, results or experience. If you could not answer three follow up questions about it, it is not your story.",
                  say="Rule two: tell only true stories. Never let AI invent skills, results or experience. If you could not answer three follow-up questions about it, it is not your story."),
             dict(card=("3   Respect the rules", "Follow employer AI policies; keep old employers' secrets"),
                  tts="Rule three: respect the rules. Follow each employer's policy on A I in applications and tasks, and keep confidential information from past employers out of every chatbot.",
                  say="Rule three: respect the rules. Follow each employer's policy on AI in applications and tasks, and keep confidential information from past employers out of every chatbot."),
         ]),
    dict(kind="title", title="Your countdown starts", year="",
         sub="Pick one step for your next interview and try it today.",
         beats=[
             dict(say="You do not need every tool here. If your interview is next week, start with one thing: write three true stories, and say them out loud tonight."),
             dict(tts="This channel is A I for Every Job. Each episode shows what A I can honestly do at work. Subscribe, and tell us in the comments which job we should cover next.",
                  say="This channel is AI for Every Job. Each episode shows what AI can honestly do at work. Subscribe, and tell us in the comments which job we should cover next."),
         ]),
]
