**Objective:**
Analyze a set of Telegram messages to detect suspicious activity, build user profiles, and assess the overall health of the conversation. Return structured information identifying any suspicious behavior, potential bots, advertising activities, or other manipulative behaviors. Additionally, provide an overall evaluation of the conversation, grading it as normal or abnormal (e.g., bot intervention or off-topic surges).

**Instructions:**
1. Conversation Analytics:

    Conversation Grade: Evaluate the entire conversation for unusual activity and categorize it as:
        Normal: Conversation is in line with the overall subject and patterns.
        Suspicious: Indicates abnormal surges, possible bot intervention, or off-topic activity.
    Provide the following metrics for the conversation:
        Total Messages: Total number of messages in the analyzed chunk.
        Active Users: Number of users who participated in the conversation (sent messages).
        Passive Users: Number of users who only forwarded messages or shared media without engaging in conversation.
        Message Frequency: Average number of messages per user per day.
        Surge in Activity: Indicate any periods of unusually high activity (e.g., more than double the average messages in a specific timeframe).
        Off-Topic Percentage: Estimate the percentage of messages that are off-topic or irrelevant.
    Consider the following when grading:
        Sudden surges in activity (e.g., a large number of messages in a short time).
        Presence of repetitive or off-topic messages.
        Large volume of links, advertisements, or hate speech.
        High number of new users joining or forwarding content without context.

2. Suspicious Activity:

    Bots: Identify potential bots based on repetitive, irrelevant, or out-of-context messages.
    Advertising or Spam:
        Detect promotional content, referral links, or unsolicited advertisements.
        Flag messages containing links or URLs, distinguishing between normal and suspicious ones (e.g., shortened links, promotional URLs).
        Specifically consider messages like:
            “Удаленная работа! От 350$ в неделю за пару часов в день! Только крипта!”
            This type of message is flagged as spam due to its promotional nature, offering jobs or services with vague claims and emphasis on cryptocurrency.
    Hate Speech: Detect hate speech while separating emotional reactions to current events from harmful behavior.
    Repetitive Messages: Flag instances of similar or repeated messages with slight variations.
    Minimal or Irregular Engagement: Flag users exhibiting minimal engagement, e.g., only forwarding messages, sharing media, or posting irrelevant content.

3. User Profiles:

    For each user, create a detailed profile based on their behavior, including:
        User Activity:
            Number of Messages: Per day and per month.
                0-10 messages/day: Low activity.
                11-50 messages/day: Average activity.
                51+ messages/day: High activity.
            Message Frequency: Number of posts per day.
                0.1-0.5/day: Low.
                0.6-3/day: Average.
                4+/day: High.
        Message Tone: Scale from 0 to 10.
            Positive: 0 (always negative) to 10 (always positive).
            Neutral: 0 (never neutral) to 10 (always neutral).
            Negative: 0 (never negative) to 10 (always negative).
        Bot Similarity: Scale from 1 to 10.
            1-3: Low similarity.
            4-7: Medium similarity.
            8-10: High similarity.
        Thematic Variety:
            Low: 1-2 topics.
            Average: 3-5 topics.
            High: 6+ topics.
        Engagement in Dialogue:
            Low: Rarely engages in dialogue.
            Average: Sometimes enters dialogues.
            High: Often enters into dialogues.
        Initiative (Questions):
            Low: 0-0.5 questions per message.
            Average: 0.6-1.5 questions per message.
            High: 1.6+ questions per message.
        Mentions of Others:
            Rarely: 0-1 mentions.
            Sometimes: 2-5 mentions.
            Frequently: 6+ mentions.
    Include usernames and IDs to provide clarity in the profile summary.

4. Structure of Output:

    Conversation Analytics: Provide an overall assessment of the conversation, including:
        Grade: [Normal/Suspicious]
        Reason: [E.g., sudden surge in activity, repetitive messages, high link volume, etc.]
        Total Messages: [X]
        Active Users: [X]
        Passive Users: [X]
        Average Messages per User: [X]
        Surge Activity Detected: [Yes/No]
        Off-Topic Percentage: [X%]
    Suspicious Activity: List detected suspicious behaviors with examples (message IDs, content, usernames, IDs, and reasons for suspicion).
    User Profiles: Provide a detailed description for each user based on the above profiling criteria.

**Input:**
Chunk of messages in this format:
```
MESSAGES
```

**Return the analysis in the following format:**
```
**Conversation Analytics:**
- **Grade**: [Normal/Suspicious]
- **Reason**: [E.g., sudden surge in activity, repetitive messages, high link volume, etc.]
- **Total Messages**: [X]
- **Active Users**: [X]
- **Passive Users**: [X]
- **Average Messages per User**: [X]
- **Surge Activity Detected**: [Yes/No]
- **Off-Topic Percentage**: [X%]

**Suspicious Activity:**
- [Message ID] - **User (Username/ID)**: [Reason for suspicion (e.g., bot, spam, irrelevant message, hate speech, suspicious link, etc.)].

**User Profiles:**
- **User (Username/ID)**: 
   - Number of Messages: [X/day, X/month] (Low/Average/High activity)
   - Message Frequency: [X/day] (Low/Average/High)
   - Message Tone: [Positive: X, Neutral: X, Negative: X]
   - Similarity to Bot: [X] (Low/Medium/High)
   - Thematic Variety: [Low/Average/High]
   - Engagement in Dialogue: [Low/Average/High]
   - Average Questions per Message: [X] (Low/Average/High initiative)
   - Mentions of Others: [X] (Rarely/Sometimes/Frequently)
```

**Output Example:**
```
**Conversation Analytics:**
- **Grade**: Suspicious
- **Reason**: Sudden surge in repetitive messages, several users sharing suspicious links.
- **Total Messages**: 250
- **Active Users**: 30
- **Passive Users**: 10
- **Average Messages per User**: 8.33
- **Surge Activity Detected**: Yes
- **Off-Topic Percentage**: 15%

**Suspicious Activity:**
- 607341 - **Oleg T. (123456)**: Possible advertising, mentions legal alcohol delivery services in a promotional tone.
- 607427 - **IvanP12 (7891011)**: Bot-like behavior, repetitive irrelevant media sharing without context.
- 607511 - **User123 (987654)**: Hate speech, aggressive comments toward a specific group.
- 607812 - **Sasha_FWD (543210)**: Spam message, offers vague job opportunities with cryptocurrency.
- 608221 - **AnnaB (332211)**: Repeated message pattern, shares variations of the same phrase multiple times.

**User Profiles:**
- **Oleg T. (123456)**: 
   - Number of Messages: 5/day, 150/month (Low activity)
   - Message Frequency: 0.3/day (Low)
   - Message Tone: Positive: 7, Neutral: 2, Negative: 1
   - Similarity to Bot: 5 (Medium)
   - Thematic Variety: Low
   - Engagement in Dialogue: Low
   - Average Questions per Message: 0.1 (Low initiative)
   - Mentions of Others: Rarely (1 mention)
- **IvanP12 (7891011)**: 
   - Number of Messages: 20/day, 600/month (Average activity)
   - Message Frequency: 2/day (Average)
   - Message Tone: Positive: 4, Neutral: 5, Negative: 1
   - Similarity to Bot: 7 (Medium)
   - Thematic Variety: Average
   - Engagement in Dialogue: Medium
   - Average Questions per Message: 0.8 (Average initiative)
   - Mentions of Others: Sometimes (4 mentions)
```
