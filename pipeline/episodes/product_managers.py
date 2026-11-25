"""Episode: AI for Product Managers in 2026.
Each scene: kind, number, title, beats. Each beat: say (narration), optional tts (pronunciation override),
optional card (name, description) or tip (text) that appears when the beat starts."""

CHANNEL = "AI for Every Job"
PRESENTER = "product_manager"
VOICE = "af_bella"
EPISODE = "AI for Product Managers in 2026"

SCENES = [
    dict(kind="title", title="AI for Product Managers", year="2026",
         sub="Seven questions every feature has to answer.",
         beats=[
             dict(tts="I'm a product manager. My job is not writing tickets, it is making sure we build the right thing. In 2026, A I helps with most of it.",
                  say="I'm a product manager. My job is not writing tickets, it is making sure we build the right thing. In 2026, AI helps with most of it."),
             dict(tts="Instead of a tool tour, I'll use seven questions every feature has to answer, from who it is for to what we learned, and show where A I fits.",
                  say="Instead of a tool tour, I'll use seven questions every feature has to answer, from who it is for to what we learned, and show where AI fits."),
             dict(say="My example is Pantry, a made up recipe app, and one request: a shopping list the whole family can share. Honest limits along the way, and three rules at the end."),
         ]),
    dict(kind="cards", num="01", title="Who is it for?",
         beats=[
             dict(say="Question one: who is it for? Sales says families want sharing. But which families, doing what? Before any research, I write down what I believe."),
             dict(card=("A Claude project", "Strategy, personas and past research in one place"),
                  say="I keep a Claude project for Pantry. Its knowledge holds our strategy, personas, and research summaries. Its instructions say: answer as a sceptical colleague and name your assumptions."),
             # Verified: https://support.claude.com/en/articles/9517075-what-are-projects
             dict(card=("List the assumptions", "Who, when, and what they do today instead"),
                  say="Then I ask: for a shared family shopping list, what are we assuming about who uses it, when, and what they do today instead? It finds some I missed."),
             dict(card=("Pick a first user", "Narrow segments, and what must be true for each"),
                  tts="Finally: suggest three narrow segments to serve first, and what must be true for each. I choose parents planning the weekly shop together. A I only widened my options.",
                  say="Finally: suggest three narrow segments to serve first, and what must be true for each. I choose parents planning the weekly shop together. AI only widened my options."),
         ]),
    dict(kind="cards", num="02", title="What problem, exactly?",
         beats=[
             dict(tts="Question two: what problem, exactly? That means talking to customers. I run a round of interviews, and A I saves me hours afterwards, sorting what people said.",
                  say="Question two: what problem, exactly? That means talking to customers. I run a round of interviews, and AI saves me hours afterwards, sorting what people said."),
             dict(card=("Notion AI Meeting Notes", "Transcript, summary and action items, with consent"),
                  tts="On Notion's Business and Enterprise plans, A I Meeting Notes transcribes the call and summarises key points and action items. Notion asks you to get consent first. So do I.",
                  say="On Notion's Business and Enterprise plans, AI Meeting Notes transcribes the call and summarises key points and action items. Notion asks you to get consent first. So do I."),
             # Verified: https://www.notion.com/help/ai-meeting-notes
             dict(card=("Dovetail", "Summaries, themes and sentiment across interviews"),
                  say="The anonymised transcripts go into Dovetail, which can summarise key takeaways, cluster highlights into themes, and flag sentiment. I still check each theme against what people actually said."),
             # Verified: https://dovetail.com/ai
             dict(card=("Ask what does not fit", "Look for the people who break the pattern"),
                  say="Then the opposite question: which interviews do not fit these themes? One dad never shops with a list at all. Outliers like him are often where the real insight hides."),
         ]),
    dict(kind="cards", num="03", title="What is the evidence?",
         beats=[
             dict(say="Question three: what is the evidence? A handful of friendly interviews is not proof. I want to see the problem in feedback we already have, from people I never met."),
             dict(card=("Productboard Spark", "Analyses feedback and links findings to the source"),
                  tts="Our feedback lives in Productboard, and its A I agent, Spark, can analyse all of it and link each finding back to the original feedback. That link is what I trust.",
                  say="Our feedback lives in Productboard, and its AI agent, Spark, can analyse all of it and link each finding back to the original feedback. That link is what I trust."),
             # Verified: https://www.productboard.com/product/spark/
             dict(card=("Check every quote", "AI can invent or blend quotes, so open the source"),
                  tts="Because A I summaries can invent a quote, or blend two customers into one. Before a quote goes on any slide, I open the original and check a real person said it.",
                  say="Because AI summaries can invent a quote, or blend two customers into one. Before a quote goes on any slide, I open the original and check a real person said it."),
             dict(card=("Figma Make", "A working prototype from a prompt and your designs"),
                  say="Then I test the idea itself. In Figma Make, I describe the shared list and attach our design frames. It builds a working prototype I can show customers this week."),
             # Verified: https://help.figma.com/hc/en-us/articles/31304485164695-Create-and-edit-a-functional-prototype-or-web-app
         ]),
    dict(kind="cards", num="04", title="What do we build first?",
         beats=[
             dict(tts="Question four: what do we build first? Everyone has an opinion, and the roadmap is full. This is where I lean on A I the least, and only as a thinking partner.",
                  say="Question four: what do we build first? Everyone has an opinion, and the roadmap is full. This is where I lean on AI the least, and only as a thinking partner."),
             dict(card=("Argue both sides", "The case for and against, then you decide"),
                  say="I paste the evidence and the other roadmap candidates and ask: make the strongest case for building this now, then the strongest case against. The ranking stays with me."),
             dict(card=("Draft the PRD", "Problem, users, scope, out of scope, open questions"),
                  tts="Once we commit, I ask for a first P R D: problem, users, scope, out of scope, open questions. Then: which edge cases did I miss, like two people ticking one item?",
                  say="Once we commit, I ask for a first PRD: problem, users, scope, out of scope, open questions. Then: which edge cases did I miss, like two people ticking one item?"),
             dict(card=("Rovo in Confluence", "Drafts Jira epics and stories from your brief"),
                  say="The spec lives in Confluence, where Rovo can draft the Jira breakdown from it: epics, stories, and tasks linked back to the page. The engineers and I review them first."),
             # Verified: https://www.atlassian.com/collections/teamwork/guides/integrations
             dict(tip="Let AI explain the trade-offs. Never let it pick your priorities.",
                  tts="An honest warning: A I sounds sure of itself, but it does not know your strategy, your team, or your customers. Let it explain trade offs. Never let it pick your priorities.",
                  say="An honest warning: AI sounds sure of itself, but it does not know your strategy, your team, or your customers. Let it explain trade offs. Never let it pick your priorities."),
         ]),
    dict(kind="cards", num="05", title="How will we know?",
         beats=[
             dict(say="Question five: how will we know it worked? I decide that before we build, not after, so nobody can quietly pick the numbers that make the feature look good."),
             dict(card=("Define success first", "One main signal, plus guardrails"),
                  say="I ask: suggest one main success signal for a shared list, and two guardrails that would warn us we broke something. Then I check we can actually measure each one."),
             dict(card=("Amplitude Global Agent", "Ask product questions in chat, get charts back"),
                  say="After launch, Amplitude's Global Agent lets me ask in plain words: how many families created a shared list each week since launch? It answers with a chart I can explore."),
             # Verified: https://amplitude.com/docs/amplitude-ai/agents-overview
             dict(card=("ChatGPT data analysis", "Upload an approved export, get tables and charts"),
                  tts="For an experiment export, if my company allows it, Chat G P T can analyse the spreadsheet by writing and running code, and draw charts. An analyst checks the result, because A I can be confidently wrong.",
                  say="For an experiment export, if my company allows it, ChatGPT can analyse the spreadsheet by writing and running code, and draw charts. An analyst checks the result, because AI can be confidently wrong."),
             # Verified: https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt
         ]),
    dict(kind="cards", num="06", title="Who needs to hear?",
         beats=[
             dict(say="Question six: who needs to hear about it? A feature nobody knows about has not really launched. Leaders, sales, support, and customers each need a different version of the news."),
             dict(card=("One update, many readers", "Same facts, different depth for each audience"),
                  say="I write the facts once, then ask: rewrite this in five lines for leadership, as likely questions and answers for support, and as what changed for buyers, for sales."),
             dict(card=("Launch notes", "What changed, why it helps, how to try it"),
                  say="For customers, I ask for launch notes in plain words: what changed, why it helps, and how to try it. Then I cut anything that overpromises."),
             dict(card=("Rehearse the hard questions", "Let the assistant play a sceptical stakeholder"),
                  say="Before the review, I ask: you are our sceptical finance director. What three hard questions will you ask about this launch? I prepare the answers myself."),
         ]),
    dict(kind="cards", num="07", title="What did we learn?",
         beats=[
             dict(say="Question seven: what did we learn? A few weeks after launch, I sit down with the results, fresh feedback, and my assumptions from question one."),
             dict(card=("Prediction versus reality", "Which assumptions held, and what surprised us"),
                  say="I paste my assumptions and the results and ask: which held, which were wrong, and what surprised us? In our made up story, couples used the shared list more than families."),
             dict(card=("Keep, change or stop", "Draft the options, then the team decides"),
                  say="Then I ask for three options, keep it, change it, or stop it, with the evidence for each. The team decides together, and I write down why."),
             dict(card=("Feed the project", "Add what you learned to the product's knowledge"),
                  say="That note goes back into the Claude project from question one. Next time someone asks for sharing, the assistant already knows what we learned, and so does the team."),
             # Verified: https://support.claude.com/en/articles/9517075-what-are-projects
         ]),
    dict(kind="cards", num="★", title="Three rules",
         beats=[
             dict(tts="Finally, three rules for every product manager using A I. Whatever tools your company chooses, these keep your customers safe and your product decisions in human hands.",
                  say="Finally, three rules for every product manager using AI. Whatever tools your company chooses, these keep your customers safe and your product decisions in human hands."),
             dict(card=("1   Customer data stays safe", "Anonymise research, approved tools only"),
                  tts="Rule one: customer data stays safe. Anonymise interviews and feedback, follow your company's A I policy, and never paste personal details into a tool it has not approved.",
                  say="Rule one: customer data stays safe. Anonymise interviews and feedback, follow your company's AI policy, and never paste personal details into a tool it has not approved."),
             dict(card=("2   People set priorities", "AI explains the trade-offs, people decide"),
                  tts="Rule two: people set priorities. A I can summarise, draft, and argue both sides. What we build, for whom, and when, is decided by people who answer for the result.",
                  say="Rule two: people set priorities. AI can summarise, draft, and argue both sides. What we build, for whom, and when, is decided by people who answer for the result."),
             dict(card=("3   Trace it to the source", "Every quote, theme and number, checked"),
                  say="Rule three: trace it to the source. Every quote, theme, and number should lead back to a real customer or a real data point. If it does not, cut it."),
         ]),
    dict(kind="title", title="Start with one question", year="",
         sub="Pick one of the seven questions and try AI on it this week.",
         beats=[
             dict(tts="You do not need A I for all seven questions at once. Pick the one that costs you the most time, maybe research synthesis or stakeholder updates, and start there.",
                  say="You do not need AI for all seven questions at once. Pick the one that costs you the most time, maybe research synthesis or stakeholder updates, and start there."),
             dict(tts="This is A I for Every Job, where each episode tests what A I can honestly do for one profession. Subscribe, and tell us in the comments which job we should cover next.",
                  say="This is AI for Every Job, where each episode tests what AI can honestly do for one profession. Subscribe, and tell us in the comments which job we should cover next."),
         ]),
]
