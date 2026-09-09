require("dotenv").config();

const { Client, GatewayIntentBits } = require("discord.js");
const {
    joinVoiceChannel,
    entersState,
    VoiceConnectionStatus,
} = require("@discordjs/voice");

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildVoiceStates,
    ],
});

let connection = null;

async function connectToVoice() {
    try {
        const guild = await client.guilds.fetch(process.env.GUILD_ID);

        const channel = await guild.channels.fetch(
            process.env.VOICE_CHANNEL_ID
        );

        if (!channel) {
            console.log("Voice Channel tidak ditemukan.");
            return;
        }

        connection = joinVoiceChannel({
            channelId: channel.id,
            guildId: guild.id,
            adapterCreator: guild.voiceAdapterCreator,
            selfDeaf: true,
            selfMute: false,
        });

        console.log(`Berhasil masuk ke Voice Channel: ${channel.name}`);

        connection.on(VoiceConnectionStatus.Disconnected, async () => {
            console.log("Bot terputus dari Voice Channel.");

            try {
                await Promise.race([
                    entersState(
                        connection,
                        VoiceConnectionStatus.Signalling,
                        5000
                    ),
                    entersState(
                        connection,
                        VoiceConnectionStatus.Connecting,
                        5000
                    ),
                ]);

                console.log("Berhasil reconnect.");
            } catch (error) {
                console.log(
                    "Reconnect gagal. Mencoba masuk kembali..."
                );

                setTimeout(connectToVoice, 5000);
            }
        });

    } catch (error) {
        console.error("Terjadi error:", error);

        setTimeout(connectToVoice, 5000);
    }
}

client.once("ready", async () => {
    console.log(`Bot aktif sebagai ${client.user.tag}`);

    await connectToVoice();
});

client.login(process.env.DISCORD_TOKEN);