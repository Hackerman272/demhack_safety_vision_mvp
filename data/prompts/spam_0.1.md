## Objective
Analyze a set of Telegram messages to detect suspicious activity and assess the overall health of the conversation. Return structured information identifying any suspicious behavior, potential bots, advertising activities, or other manipulative behaviors. Additionally, provide an overall evaluation of the conversation, grading it as normal or abnormal (e.g., bot intervention or off-topic surges).

## Instructions

### Conversation Analytics

#### Conversation Grade
Evaluate the entire conversation for unusual activity and categorize it as:
**Normal**: Conversation is in line with the overall subject and patterns.
**Suspicious**: Indicates abnormal surges, possible bot intervention, or off-topic activity.

#### Provide the following metrics for the conversation
**Total Messages**: Total number of messages in the analyzed chunk.
**Active Users**: Number of users who participated in the conversation (sent messages).
**Passive Users**: Number of users who only forwarded messages or shared media without engaging in conversation.
**Message Frequency**: Average number of messages per user per day.
**Surge in Activity**: Indicate any periods of unusually high activity (e.g., more than double the average messages in a specific timeframe).
**Off-Topic Percentage**: Estimate the percentage of messages that are off-topic or irrelevant.

#### Consider the following when grading
- Sudden surges in activity (e.g., a large number of messages in a short time).
- Presence of repetitive or off-topic messages.
- Large volume of links, advertisements, or hate speech.
- High number of new users joining or forwarding content without context.

### Suspicious Activity
**Bots**: Identify potential bots based on repetitive, irrelevant, or out-of-context messages.
**Advertising or Spam**:
- Detect promotional content, referral links, or unsolicited advertisements.
- Flag messages containing links or URLs, distinguishing between normal and suspicious ones (e.g., shortened links, promotional URLs).
- Specifically consider messages like:
  - “Удаленная работа! От 350$ в неделю за пару часов в день! Только крипта!”
  - This type of message is flagged as spam due to its promotional nature, offering jobs or services with vague claims and emphasis on cryptocurrency.
**Which is not spam**
 - Conversations about travelling
 - Questions about travelling
 - Travell impressions
**Hate Speech**: Detect hate speech while separating emotional reactions to current events from harmful behavior.
**Repetitive Messages**: Flag instances of similar or repeated messages with slight variations.
**Minimal or Irregular Engagement**: Flag users exhibiting minimal engagement, e.g., only forwarding messages, sharing media, or posting irrelevant content.

## Structure of Output in YAML format
```yaml
Conversation Analytics: # Provide an overall assessment of the conversation, including:
  Grade: Normal/Suspicious
  Reason: E.g., sudden surge in activity, repetitive messages, high link volume, etc.
  Total Messages: X
  Active Users: X
  Passive Users: X
  Average Messages per User: X
  Surge Activity Detected: Yes/No
  Off-Topic Percentage: X%
Suspicious Activity: List detected suspicious behaviors with examples (message IDs, content, usernames, IDs, and reasons for suspicion).
```

## Input
### Format example
```yaml
---
userID: 1111111
text: Text example 1
date: '2020-06-12 06:46:03'
---
userID: 2222222
text: Text example 2
date: '2020-06-12 07:12:32'
```

### Chunk of messages in YAML format
```yaml
"MESSAGES"
```

## Return the analysis in YAML format
```yaml
Conversation Analytics:
  Grade: Normal/Suspicious
  Reason: E.g., sudden surge in activity, repetitive messages, high link volume, etc.
  Total Messages: X
  Active Users: X
  Passive Users: X
  Average Messages per User: X
  Surge Activity Detected: Yes/No
  Off-Topic Percentage: X%

Suspicious Activity:
  [UserID]: Reason for suspicion (e.g., bot, spam, irrelevant message, hate speech, suspicious link, etc.).
```

## Output Example in YAML format
```yaml
Conversation Analytics:
  Grade: Suspicious
  Reason: Sudden surge in repetitive messages, several users sharing suspicious links.
  Total Messages: 250
  Active Users: 30
  Passive Users: 10
  Average Messages per User: 8.33
  Surge Activity Detected: Yes
  Off-Topic Percentage: 15%

Suspicious Activity of Users:
   [UserID]: Possible advertising, mentions legal alcohol delivery services in a promotional tone.
   [UserID]: Bot-like behavior, repetitive irrelevant media sharing without context.
   [UserID]: Hate speech, aggressive comments toward a specific group.
   [UserID]: Spam message, offers vague job opportunities with cryptocurrency.
   [UserID]: Repeated message pattern, shares variations of the same phrase multiple times.
```
