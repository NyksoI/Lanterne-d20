package fr.lanterne.d20.game

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import fr.lanterne.d20.widget.PnjWidget

enum class Screen { TITLE, CREATION, PLAY }

/** Un jet en attente : le joueur a choisi une option avec un test de compétence. */
data class PendingCheck(
    val choice: Choice,
    val check: Check,
    val skillName: String,
    val parts: List<BonusPart>,
    val advantage: Boolean,
) {
    val bonus: Int get() = parts.sumOf { it.value }
}

/** Le « moteur » du jeu : état courant, choix, jets, sauvegarde. */
class GameController(context: Context) {
    private val appContext = context.applicationContext
    val data: GameData = GameData.load(appContext)

    var screen by mutableStateOf(Screen.TITLE)
    var character by mutableStateOf<Character?>(null)
        private set
    var sceneId by mutableStateOf(data.start)
        private set
    var flags by mutableStateOf<Set<String>>(emptySet())
        private set
    var inspiration by mutableIntStateOf(STARTING_INSPIRATION)
        private set
    var pending by mutableStateOf<PendingCheck?>(null)
        private set

    val scene: Scene get() = data.scene(sceneId)
    val hasSave: Boolean get() = SaveStore.load(appContext) != null

    // ── Démarrage ──

    fun continueGame(): Boolean {
        val save = SaveStore.load(appContext) ?: return false
        character = Character(data, save.player)
        sceneId = if (data.scenes.containsKey(save.sceneId)) save.sceneId else data.start
        flags = save.flags
        inspiration = save.inspiration
        pending = null
        screen = Screen.PLAY
        return true
    }

    fun newGame(player: Player) {
        character = Character(data, player)
        flags = emptySet()
        inspiration = STARTING_INSPIRATION
        pending = null
        screen = Screen.PLAY
        enter(data.start)
    }

    // ── Choix ──

    fun visibleChoices(): List<Choice> {
        val c = character ?: return emptyList()
        return scene.choices.filter { ch ->
            (ch.races.isEmpty() || c.race.id in ch.races) &&
                (ch.classes.isEmpty() || c.charClass.id in ch.classes) &&
                ch.requires.all { it in flags } &&
                ch.hideIf.none { it in flags }
        }
    }

    fun choose(choice: Choice) {
        val c = character ?: return
        flags = flags + choice.set
        val check = choice.check
        if (check != null) {
            pending = PendingCheck(
                choice = choice,
                check = check,
                skillName = data.skills[check.skill]?.name ?: check.skill,
                parts = c.bonusParts(check.skill),
                advantage = check.advantage.any { it in flags },
            )
        } else {
            choice.next?.let { enter(it) }
        }
    }

    // ── Jets ──

    fun roll(p: PendingCheck): RollResult = Dice.roll(p.bonus, p.check.dc, p.advantage)

    fun spendInspiration(): Boolean {
        if (inspiration <= 0) return false
        inspiration -= 1
        persist()
        return true
    }

    fun resolve(result: RollResult) {
        val p = pending ?: return
        if (result.critical) inspiration += 1
        pending = null
        val target = if (result.success) p.choice.success else p.choice.failure
        enter(target ?: data.start)
    }

    // ── Navigation ──

    private fun enter(id: String) {
        val s = data.scene(id)
        sceneId = s.id
        flags = flags + s.set
        inspiration += s.inspiration
        persist()
    }

    fun restart() {
        SaveStore.clear(appContext)
        character = null
        pending = null
        screen = Screen.CREATION
        PnjWidget.updateAll(appContext)
    }

    private fun persist() {
        val c = character ?: return
        SaveStore.save(appContext, SaveState(c.player, sceneId, flags, inspiration))
        PnjWidget.updateAll(appContext)
    }

    companion object {
        const val STARTING_INSPIRATION = 1
    }
}
