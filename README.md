<a name="readme-top"></a>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/discord.py-2.0+-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="discord.py">
  <img src="https://img.shields.io/github/license/devan518/luna-bot?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/issues/devan518/luna-bot?style=for-the-badge" alt="Issues">
</p>

<br />

<p align="center">
  <img src="https://raw.githubusercontent.com/devan518/luna-bot/main/luna.png" width="300" height="350">
</p>

<h1 align="center">LunaBot</h1>

<p align="center">
  A Luna Snow themed Discord bot for Marvel Rivals fans!
  <br />
  <br />
  <a href="https://discord.com/oauth2/authorize?client_id=1496972614722257107&permissions=0&integration_type=0&scope=bot">
    <strong>Add to your server »</strong>
  </a>
  <br />
  <br />
  <a href="https://github.com/devan518/luna-bot/issues/new?labels=bug">report bug</a>
  ·
  <a href="https://github.com/devan518/luna-bot/issues/new?labels=enhancement">request feature (near instant response)</a>
</p>

## Table of Contents

1. [About](#about)
2. [Getting Started](#getting-started)
3. [Commands](#commands)
4. [Roadmap](#roadmap)
5. [Contributing](#contributing)

---

## About

LunaBot is a Discord bot themed around **Luna Snow** from Marvel Rivals. Her personality, responses, and features are all designed around the character!

Built with:

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
![pytubefix](https://img.shields.io/badge/pytubefix-FF0000?style=for-the-badge&logo=youtube&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

### Add to your server

Click [here](https://discord.com/oauth2/authorize?client_id=1496972614722257107&permissions=0&integration_type=0&scope=bot), select your server from the dropdown, and click **Add**.

Then give LunaBot a role with appropriate permissions — ideally your default mod role or a role with the highest position in your role list so she can assign roles correctly.

---

## Commands

### 🎭 Fun

| Command | Description |
|---|---|
| `/emote` | Luna breaks it down — pick from her Marvel Rivals emotes |
| `/lie-detect` | Luna determines whether your statement is true or not |
| `/repeat` | Luna repeats whatever you tell her to say |

### 🎵 Music

| Command | Description |
|---|---|
| `/play` | Add a song to the queue by name or URL |
| `/queue` | View the current song queue |
| `/skip` | Skip the current song |
| `/pause` | Pause playback |
| `/resume` | Resume playback |
| `/remove` | Remove a song from the queue by index |
| `/clear` | Clear the entire queue |
| `/leave` | Disconnect Luna from the voice channel |

### 🏆 Quests & Points

| Command | Description |
|---|---|
| `/quests` | View all available quests |
| `/complete_quest` | Submit a quest completion with proof for mod approval |
| `/leaderboard` | View the top 50 points leaderboard |
| `/quest` *(questmaster)* | Create a new quest |
| `/delete_quest` *(questmaster)* | Delete a quest by ID |
| `/approve_quest` *(questmaster)* | Approve a quest completion by message ID |
| `/set_points` *(questmaster)* | Set a user's points to a specific value |


> **Note:** by "questmaster" i mean the role needs to be a role exactly named "questmaster", i added this because mods could've cheated on quests and the leaderboard, 
> give this role to someone you trust 


### ⚙️ Server

| Command | Description |
|---|---|
| `/role` *(mod)* | Send a reaction role message for all server roles |
| `/sync` *(mod)* | Sync slash commands |
| `/status` | View bot status, uptime, latency, and more |


> **Note:** by "mod", i mean a role with mod permissions that is explicitly named either "Mod", "mod", or "MOD"

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Roadmap

- [x] Luna Snow emotes
- [x] Music player with queue
- [x] Quest & points system with mod approval flow
- [x] Reaction roles
- [x] Leaderboard
- [ ] Improve responses from luna to be mroe themed, looking for contributors to open issues of ideas
- [ ] More Luna-themed responses and interactions

See [open issues](https://github.com/devan518/luna-bot/issues) for a full list of proposed features and known bugs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Acknowledgments

* [discord.py](https://discordpy.readthedocs.io/)
* [pytubefix](https://github.com/JuanBindez/pytubefix)
* [TinyDB](https://tinydb.readthedocs.io/)
* [shields.io](https://shields.io)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
