package fr.lanterne.d20.game

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

/*
 * Toutes les données du jeu (races, classes, PNJ, scènes, portraits) viennent de
 * assets/game.json. Pour modifier l'histoire, il suffit de modifier ce fichier.
 */

data class Ability(val id: String, val name: String)

data class Skill(val id: String, val name: String, val ability: String)

data class Race(
    val id: String,
    val name: String,
    val desc: String,
    val bonus: Map<String, Int>,
    val skills: List<String>,
    val portrait: String,
)

data class CharClass(
    val id: String,
    val name: String,
    val desc: String,
    val scores: List<Int>,
    val skills: List<String>,
)

data class Npc(val id: String, val name: String, val race: String, val title: String, val portrait: String)

/** Un jet de compétence : compétence, difficulté, et les "flags" qui donnent l'avantage. */
data class Check(val skill: String, val dc: Int, val advantage: List<String>)

data class Choice(
    val text: String,
    val next: String?,
    val check: Check?,
    val success: String?,
    val failure: String?,
    val races: List<String>,
    val classes: List<String>,
    val requires: List<String>,
    val hideIf: List<String>,
    val set: List<String>,
)

data class Ending(val kind: String, val title: String) {
    val isVictory: Boolean get() = kind == "victoire"
}

data class Scene(
    val id: String,
    val npc: String?,
    val text: String,
    val choices: List<Choice>,
    val set: List<String>,
    val inspiration: Int,
    val end: Ending?,
)

class GameData(
    val title: String,
    val start: String,
    val abilities: List<Ability>,
    val skills: Map<String, Skill>,
    val races: List<Race>,
    val classes: List<CharClass>,
    val npcs: Map<String, Npc>,
    val portraits: Map<String, List<String>>,
    val font: Map<Char, List<String>>,
    val scenes: Map<String, Scene>,
) {
    fun race(id: String): Race = races.firstOrNull { it.id == id } ?: races.first()
    fun charClass(id: String): CharClass = classes.firstOrNull { it.id == id } ?: classes.first()
    fun scene(id: String): Scene = scenes[id] ?: scenes.getValue(start)
    fun portrait(id: String?): List<String> = portraits[id] ?: portraits.getValue("scene_lanterne")

    companion object {
        @Volatile
        private var cached: GameData? = null

        fun load(context: Context): GameData {
            cached?.let { return it }
            synchronized(this) {
                cached?.let { return it }
                val text = context.applicationContext.assets.open("game.json")
                    .bufferedReader(Charsets.UTF_8).use { it.readText() }
                val data = parse(text)
                cached = data
                return data
            }
        }

        fun parse(text: String): GameData {
            val root = JSONObject(text)

            val abilities = root.getJSONArray("abilities").objects().map {
                Ability(it.getString("id"), it.getString("name"))
            }
            val skills = root.getJSONArray("skills").objects().map {
                Skill(it.getString("id"), it.getString("name"), it.getString("ability"))
            }.associateBy { it.id }

            val races = root.getJSONArray("races").objects().map { r ->
                val bonusObj = r.getJSONObject("bonus")
                val bonus = bonusObj.keys().asSequence().associateWith { bonusObj.getInt(it) }
                Race(
                    id = r.getString("id"),
                    name = r.getString("name"),
                    desc = r.getString("desc"),
                    bonus = bonus,
                    skills = r.optJSONArray("skills").strings(),
                    portrait = r.getString("portrait"),
                )
            }

            val classes = root.getJSONArray("classes").objects().map { c ->
                val scoresArr = c.getJSONArray("scores")
                CharClass(
                    id = c.getString("id"),
                    name = c.getString("name"),
                    desc = c.getString("desc"),
                    scores = List(scoresArr.length()) { scoresArr.getInt(it) },
                    skills = c.optJSONArray("skills").strings(),
                )
            }

            val npcObj = root.getJSONObject("npcs")
            val npcs = npcObj.keys().asSequence().associateWith { id ->
                val n = npcObj.getJSONObject(id)
                Npc(id, n.getString("name"), n.getString("race"), n.getString("title"), n.getString("portrait"))
            }

            val portraitObj = root.getJSONObject("portraits")
            val portraits = portraitObj.keys().asSequence().associateWith { portraitObj.getJSONArray(it).strings() }

            val fontObj = root.getJSONObject("font")
            val font = fontObj.keys().asSequence().associate { it[0] to fontObj.getJSONArray(it).strings() }

            val nodeObj = root.getJSONObject("nodes")
            val scenes = nodeObj.keys().asSequence().associateWith { id ->
                val n = nodeObj.getJSONObject(id)
                val endObj = n.optJSONObject("end")
                Scene(
                    id = id,
                    npc = n.optStringOrNull("npc"),
                    text = n.getString("text"),
                    choices = n.optJSONArray("choices").objects().map { parseChoice(it) },
                    set = n.optJSONArray("set").strings(),
                    inspiration = n.optInt("inspiration", 0),
                    end = endObj?.let { Ending(it.getString("kind"), it.getString("title")) },
                )
            }

            return GameData(
                title = root.getString("title"),
                start = root.getString("start"),
                abilities = abilities,
                skills = skills,
                races = races,
                classes = classes,
                npcs = npcs,
                portraits = portraits,
                font = font,
                scenes = scenes,
            )
        }

        private fun parseChoice(c: JSONObject): Choice {
            val checkObj = c.optJSONObject("check")
            return Choice(
                text = c.getString("text"),
                next = c.optStringOrNull("next"),
                check = checkObj?.let {
                    Check(it.getString("skill"), it.getInt("dc"), it.optJSONArray("advantage").strings())
                },
                success = c.optStringOrNull("success"),
                failure = c.optStringOrNull("failure"),
                races = c.optJSONArray("races").strings(),
                classes = c.optJSONArray("classes").strings(),
                requires = c.optJSONArray("requires").strings(),
                hideIf = c.optJSONArray("hideIf").strings(),
                set = c.optJSONArray("set").strings(),
            )
        }
    }
}

// ── petits utilitaires JSON ──

private fun JSONArray?.strings(): List<String> =
    if (this == null) emptyList() else List(length()) { getString(it) }

private fun JSONArray?.objects(): List<JSONObject> =
    if (this == null) emptyList() else List(length()) { getJSONObject(it) }

private fun JSONObject.optStringOrNull(key: String): String? =
    if (has(key) && !isNull(key)) getString(key) else null
