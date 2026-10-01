package fr.lanterne.d20.ui

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.systemBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicText
import androidx.compose.foundation.verticalScroll
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import fr.lanterne.d20.game.Character
import fr.lanterne.d20.game.Choice
import fr.lanterne.d20.game.DotText
import fr.lanterne.d20.game.GameController
import fr.lanterne.d20.game.PendingCheck
import fr.lanterne.d20.game.RollResult
import fr.lanterne.d20.game.Scene
import fr.lanterne.d20.game.Screen
import fr.lanterne.d20.game.signed
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlin.random.Random

@Composable
fun PlayScreen(controller: GameController) {
    val pending = controller.pending
    val scene = controller.scene
    when {
        pending != null -> RollScreen(controller, pending)
        scene.end != null -> EndScreen(controller, scene)
        else -> DialogueScreen(controller, scene)
    }
}

// ─────────────────────────── DIALOGUE ───────────────────────────

@Composable
private fun DialogueScreen(controller: GameController, scene: Scene) {
    val character = controller.character ?: return
    val data = controller.data
    val npc = scene.npc?.let { data.npcs[it] }
    val scroll = rememberScrollState()
    LaunchedEffect(scene.id) { scroll.scrollTo(0) }

    Column(
        Modifier
            .fillMaxSize()
            .background(Black)
            .systemBarsPadding()
            .verticalScroll(scroll)
            .padding(horizontal = 20.dp, vertical = 12.dp),
    ) {
        TopBar(controller, character)
        Spacer(Modifier.height(18.dp))

        Box(Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
            DotGrid(data.portrait(npc?.portrait ?: "scene_lanterne"), Modifier.fillMaxWidth(0.6f))
        }
        Spacer(Modifier.height(14.dp))
        if (npc != null) {
            BasicText(
                npc.name.uppercase(), Modifier.fillMaxWidth(),
                style = style(Ink, 18.sp, FontWeight.Bold, 2.sp, TextAlign.Center),
            )
            BasicText(
                "${npc.race} · ${npc.title}", Modifier.fillMaxWidth(),
                style = style(Gray, 12.sp, align = TextAlign.Center),
            )
        } else {
            BasicText(
                "PORT-BRUME", Modifier.fillMaxWidth(),
                style = style(Gray, 12.sp, FontWeight.Bold, 2.sp, TextAlign.Center),
            )
        }
        Spacer(Modifier.height(16.dp))

        Box(
            Modifier
                .fillMaxWidth()
                .border(1.dp, Line, RoundedCornerShape(22.dp))
                .padding(18.dp),
        ) {
            BasicText(character.fill(scene.text), style = style(size = 16.sp, lineHeight = 25.sp))
        }
        Spacer(Modifier.height(12.dp))

        controller.visibleChoices().forEachIndexed { i, choice ->
            ChoiceRow(i + 1, choice, controller, character)
        }
        Spacer(Modifier.height(24.dp))
    }
}

@Composable
private fun TopBar(controller: GameController, character: Character) {
    Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
        DotGrid(controller.data.portrait(character.race.portrait), Modifier.width(30.dp))
        Spacer(Modifier.width(10.dp))
        Column(Modifier.weight(1f)) {
            BasicText(character.player.name.uppercase(), style = style(Ink, 13.sp, FontWeight.Bold, 1.sp))
            BasicText("${character.race.name} · ${character.charClass.name}", style = style(Gray, 11.sp))
        }
        InspirationDots(controller.inspiration)
        Spacer(Modifier.width(14.dp))
        Caps("Menu", Modifier.clickable { controller.screen = Screen.TITLE }.padding(6.dp))
    }
}

@Composable
private fun ChoiceRow(number: Int, choice: Choice, controller: GameController, character: Character) {
    val data = controller.data
    val tags = buildList {
        if (choice.races.isNotEmpty()) add(character.race.name.uppercase())
        if (choice.classes.isNotEmpty()) add(character.charClass.name.uppercase())
        choice.check?.let { add(data.skills[it.skill]?.name?.uppercase() ?: it.skill) }
    }
    val advantage = choice.check?.advantage?.any { it in controller.flags } == true

    Column(Modifier.fillMaxWidth()) {
        Box(Modifier.fillMaxWidth().height(1.dp).background(Line))
        Row(
            Modifier
                .fillMaxWidth()
                .clickable { controller.choose(choice) }
                .padding(vertical = 14.dp),
        ) {
            BasicText("$number.", Modifier.width(30.dp), style = style(Gray, 15.sp, FontWeight.Bold))
            Column(Modifier.weight(1f)) {
                if (tags.isNotEmpty()) {
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        tags.forEach { BasicText("[$it]", style = style(Red, 11.sp, FontWeight.Bold, 1.sp)) }
                        if (advantage) BasicText("▲ AVANTAGE", style = style(Ink, 11.sp, FontWeight.Bold, 1.sp))
                    }
                    Spacer(Modifier.height(4.dp))
                }
                BasicText(character.fill(choice.text), style = style(size = 15.sp, lineHeight = 22.sp))
            }
        }
    }
}

// ─────────────────────────── JET DE DÉ ───────────────────────────

private enum class RollPhase { READY, ROLLING, DONE }

@Composable
private fun RollScreen(controller: GameController, p: PendingCheck) {
    val font = controller.data.font
    val haptic = LocalHapticFeedback.current
    var phase by remember(p) { mutableStateOf(RollPhase.READY) }
    var shown by remember(p) { mutableIntStateOf(20) }
    var result by remember(p) { mutableStateOf<RollResult?>(null) }
    var rerolled by remember(p) { mutableStateOf(false) }
    var rollCount by remember(p) { mutableIntStateOf(0) }
    val spin = remember(p) { Animatable(0f) }

    LaunchedEffect(p, rollCount) {
        if (rollCount == 0) return@LaunchedEffect
        phase = RollPhase.ROLLING
        result = null
        val r = controller.roll(p)
        launch { spin.animateTo(spin.value + 720f, tween(1100, easing = FastOutSlowInEasing)) }
        repeat(16) { i ->
            shown = Random.nextInt(1, 21)
            delay(30L + i * 6L)
        }
        shown = r.kept
        result = r
        phase = RollPhase.DONE
        haptic.performHapticFeedback(HapticFeedbackType.LongPress)
    }

    val r = result
    val ink = when {
        r == null -> '#'
        r.success -> '#'
        else -> 'r'
    }
    val diceColor = when {
        r == null -> Line
        r.critical -> Ink
        r.success -> Gray
        else -> Red
    }

    Column(
        Modifier
            .fillMaxSize()
            .background(Black)
            .systemBarsPadding()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Caps("Jet de ${p.skillName}", color = Ink, size = 14.sp)
        Spacer(Modifier.height(18.dp))
        Caps("Difficulté")
        Spacer(Modifier.height(8.dp))
        DotGrid(DotText.rows(font, p.check.dc.toString(), 'r'), Modifier.width(54.dp), showEmpty = false)

        Spacer(Modifier.weight(1f))

        Box(
            Modifier
                .fillMaxWidth(0.82f)
                .clickable(enabled = phase == RollPhase.READY) { rollCount += 1 },
            contentAlignment = Alignment.Center,
        ) {
            D20Shape(Modifier.fillMaxWidth().graphicsLayer { rotationZ = spin.value }, color = diceColor)
            val digits = DotText.rows(font, shown.toString(), ink)
            DotGrid(
                digits,
                Modifier
                    .fillMaxWidth(digits[0].length * 0.036f)
                    .background(Black)
                    .padding(6.dp),
                showEmpty = false,
            )
        }

        Spacer(Modifier.weight(1f))

        when (phase) {
            RollPhase.READY -> {
                BasicText(
                    "d20 ${signed(p.bonus)}",
                    style = style(Ink, 22.sp, FontWeight.Bold, align = TextAlign.Center),
                )
                Spacer(Modifier.height(4.dp))
                BasicText(
                    p.parts.joinToString("   ") { "${it.label} ${signed(it.value)}" },
                    style = style(Gray, 12.sp, align = TextAlign.Center),
                )
                if (p.advantage) {
                    Spacer(Modifier.height(8.dp))
                    BasicText(
                        "▲ AVANTAGE : deux dés, on garde le meilleur",
                        style = style(Red, 12.sp, FontWeight.Bold, align = TextAlign.Center),
                    )
                }
                Spacer(Modifier.height(24.dp))
                NButton("Lancer le d20", Modifier.fillMaxWidth()) { rollCount += 1 }
            }

            RollPhase.ROLLING -> {
                Caps("Le dé roule…")
                Spacer(Modifier.height(64.dp))
            }

            RollPhase.DONE -> if (r != null) {
                val verdict = when {
                    r.critical -> "CRITIQUE !"
                    r.fumble -> "ÉCHEC CRITIQUE"
                    r.success -> "RÉUSSITE"
                    else -> "ÉCHEC"
                }
                DotGrid(
                    DotText.rows(font, verdict, if (r.success) '#' else 'r'),
                    Modifier.fillMaxWidth(if (verdict.length > 9) 0.95f else 0.7f),
                    showEmpty = false,
                )
                Spacer(Modifier.height(12.dp))
                BasicText(
                    "${r.kept} ${signed(r.bonus)} = ${r.total}   ·   DD ${r.dc}",
                    style = style(Ink, 14.sp, align = TextAlign.Center),
                )
                if (r.dice.size > 1) {
                    BasicText(
                        "Dés : ${r.dice.joinToString(" / ")}",
                        style = style(Gray, 12.sp, align = TextAlign.Center),
                    )
                }
                if (r.critical) {
                    BasicText("+1 inspiration", style = style(Red, 12.sp, FontWeight.Bold))
                }
                Spacer(Modifier.height(20.dp))
                if (!r.success && !rerolled && controller.inspiration > 0) {
                    NButton("Relancer · 1 inspiration", Modifier.fillMaxWidth(), primary = false) {
                        if (controller.spendInspiration()) {
                            rerolled = true
                            rollCount += 1
                        }
                    }
                    Spacer(Modifier.height(10.dp))
                }
                NButton("Continuer", Modifier.fillMaxWidth()) { controller.resolve(r) }
            }
        }
    }
}

// ─────────────────────────── FIN ───────────────────────────

@Composable
private fun EndScreen(controller: GameController, scene: Scene) {
    val character = controller.character ?: return
    val data = controller.data
    val end = scene.end ?: return
    val npc = scene.npc?.let { data.npcs[it] }

    Column(
        Modifier
            .fillMaxSize()
            .background(Black)
            .systemBarsPadding()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Spacer(Modifier.height(24.dp))
        DotGrid(
            DotText.rows(data.font, if (end.isVictory) "VICTOIRE" else "DEFAITE", if (end.isVictory) '#' else 'r'),
            Modifier.fillMaxWidth(),
            showEmpty = false,
        )
        Spacer(Modifier.height(14.dp))
        Caps(end.title, color = if (end.isVictory) Red else Gray, size = 13.sp)
        Spacer(Modifier.height(24.dp))
        DotGrid(data.portrait(npc?.portrait ?: character.race.portrait), Modifier.fillMaxWidth(0.45f))
        Spacer(Modifier.height(24.dp))
        Box(
            Modifier
                .fillMaxWidth()
                .border(1.dp, Line, RoundedCornerShape(22.dp))
                .padding(18.dp),
        ) {
            BasicText(character.fill(scene.text), style = style(size = 16.sp, lineHeight = 25.sp))
        }
        Spacer(Modifier.height(28.dp))
        NButton("Nouvelle aventure", Modifier.fillMaxWidth()) { controller.restart() }
        Spacer(Modifier.height(10.dp))
        NButton("Menu", Modifier.fillMaxWidth(), primary = false) { controller.screen = Screen.TITLE }
    }
}
