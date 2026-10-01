package fr.lanterne.d20.game

import android.content.Context
import kotlin.random.Random

/** Le personnage créé par le joueur. */
data class Player(val name: String, val raceId: String, val classId: String)

/** Une ligne du détail d'un bonus, ex. « Charisme +2 ». */
data class BonusPart(val label: String, val value: Int)

/** Résultat d'un jet de d20 façon Baldur's Gate. */
data class RollResult(
    val dice: List<Int>,      // 1 dé, ou 2 avec l'avantage
    val kept: Int,            // le dé gardé
    val bonus: Int,
    val dc: Int,
) {
    val total: Int get() = kept + bonus
    val critical: Boolean get() = kept == 20
    val fumble: Boolean get() = kept == 1
    /** 20 naturel = réussite automatique, 1 naturel = échec automatique. */
    val success: Boolean get() = critical || (!fumble && total >= dc)
}

/** Règles D&D 5e simplifiées : caractéristiques, modificateurs, maîtrise. */
class Character(val data: GameData, val player: Player) {
    val race: Race = data.race(player.raceId)
    val charClass: CharClass = data.charClass(player.classId)

    fun score(abilityId: String): Int {
        val index = data.abilities.indexOfFirst { it.id == abilityId }
        val base = charClass.scores.getOrElse(index) { 10 }
        return base + (race.bonus[abilityId] ?: 0)
    }

    fun modifier(abilityId: String): Int = (score(abilityId) - 10).floorDiv(2)

    fun isProficient(skillId: String): Boolean = skillId in charClass.skills || skillId in race.skills

    fun bonusParts(skillId: String): List<BonusPart> {
        val skill = data.skills[skillId] ?: return emptyList()
        val abilityName = data.abilities.firstOrNull { it.id == skill.ability }?.name ?: skill.ability
        val parts = mutableListOf(BonusPart(abilityName, modifier(skill.ability)))
        if (isProficient(skillId)) parts += BonusPart("Maîtrise", PROFICIENCY)
        return parts
    }

    fun skillBonus(skillId: String): Int = bonusParts(skillId).sumOf { it.value }

    /** Remplace {nom}, {race}, {classe} dans les textes. */
    fun fill(text: String): String = text
        .replace("{nom}", player.name)
        .replace("{race}", race.name.lowercase())
        .replace("{classe}", charClass.name.lowercase())

    companion object {
        const val PROFICIENCY = 2
    }
}

object Dice {
    fun d20(random: Random = Random.Default): Int = random.nextInt(1, 21)

    fun roll(bonus: Int, dc: Int, advantage: Boolean, random: Random = Random.Default): RollResult {
        val dice = if (advantage) listOf(d20(random), d20(random)) else listOf(d20(random))
        return RollResult(dice = dice, kept = dice.max(), bonus = bonus, dc = dc)
    }
}

fun signed(value: Int): String = if (value >= 0) "+$value" else "$value"

/** Sauvegarde dans les SharedPreferences, partagée entre l'app et le widget. */
data class SaveState(
    val player: Player,
    val sceneId: String,
    val flags: Set<String>,
    val inspiration: Int,
)

object SaveStore {
    private const val PREFS = "lanterne_save"
    private const val K_NAME = "name"
    private const val K_RACE = "race"
    private const val K_CLASS = "class"
    private const val K_SCENE = "scene"
    private const val K_FLAGS = "flags"
    private const val K_INSPIRATION = "inspiration"
    private const val K_WIDGET_ROLL = "widget_roll"

    private fun prefs(context: Context) =
        context.applicationContext.getSharedPreferences(PREFS, Context.MODE_PRIVATE)

    fun load(context: Context): SaveState? {
        val p = prefs(context)
        val name = p.getString(K_NAME, null) ?: return null
        val race = p.getString(K_RACE, null) ?: return null
        val cls = p.getString(K_CLASS, null) ?: return null
        val scene = p.getString(K_SCENE, null) ?: return null
        val flags = p.getString(K_FLAGS, "").orEmpty().split(',').filter { it.isNotBlank() }.toSet()
        return SaveState(Player(name, race, cls), scene, flags, p.getInt(K_INSPIRATION, 1))
    }

    fun save(context: Context, state: SaveState) {
        prefs(context).edit()
            .putString(K_NAME, state.player.name)
            .putString(K_RACE, state.player.raceId)
            .putString(K_CLASS, state.player.classId)
            .putString(K_SCENE, state.sceneId)
            .putString(K_FLAGS, state.flags.joinToString(","))
            .putInt(K_INSPIRATION, state.inspiration)
            .apply()
    }

    fun clear(context: Context) {
        val roll = widgetRoll(context)
        prefs(context).edit().clear().putInt(K_WIDGET_ROLL, roll).apply()
    }

    /** 0 = pas encore lancé. */
    fun widgetRoll(context: Context): Int = prefs(context).getInt(K_WIDGET_ROLL, 0)

    fun setWidgetRoll(context: Context, value: Int) {
        prefs(context).edit().putInt(K_WIDGET_ROLL, value).apply()
    }
}
