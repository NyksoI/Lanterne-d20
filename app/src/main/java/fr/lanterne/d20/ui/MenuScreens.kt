package fr.lanterne.d20.ui

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
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicText
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import fr.lanterne.d20.game.CharClass
import fr.lanterne.d20.game.Character
import fr.lanterne.d20.game.DotText
import fr.lanterne.d20.game.GameController
import fr.lanterne.d20.game.Player
import fr.lanterne.d20.game.Race
import fr.lanterne.d20.game.Screen
import fr.lanterne.d20.game.signed

// ─────────────────────────── ÉCRAN TITRE ───────────────────────────

@Composable
fun TitleScreen(controller: GameController) {
    val data = controller.data
    val hasSave = remember { controller.hasSave }
    Column(
        Modifier
            .fillMaxSize()
            .background(Black)
            .systemBarsPadding()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        DotGrid(data.portrait("scene_lanterne"), Modifier.fillMaxWidth(0.5f))
        Spacer(Modifier.height(28.dp))
        DotGrid(DotText.rows(data.font, "LANTERNE"), Modifier.fillMaxWidth(), showEmpty = false)
        Spacer(Modifier.height(10.dp))
        DotGrid(DotText.rows(data.font, "D'AUBE", 'r'), Modifier.fillMaxWidth(0.42f), showEmpty = false)
        Spacer(Modifier.height(18.dp))
        Caps("Un jeu de dialogue à coups de d20")
        Spacer(Modifier.height(48.dp))
        if (hasSave) {
            NButton("Continuer", Modifier.fillMaxWidth()) { controller.continueGame() }
            Spacer(Modifier.height(12.dp))
        }
        NButton("Nouvelle partie", Modifier.fillMaxWidth(), primary = !hasSave) {
            controller.screen = Screen.CREATION
        }
        Spacer(Modifier.height(32.dp))
        // une petite procession de races en bas de l'écran
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            listOf("tieffelin", "nain", "elfe", "drakeide", "tabaxi").forEach {
                DotGrid(data.portrait(it), Modifier.width(44.dp))
            }
        }
    }
}

// ─────────────────────────── CRÉATION DU PERSONNAGE ───────────────────────────

@Composable
fun CreationScreen(controller: GameController) {
    val data = controller.data
    var name by remember { mutableStateOf("") }
    var raceId by remember { mutableStateOf(data.races.first { it.id == "tieffelin" }.id) }
    var classId by remember { mutableStateOf(data.classes.first().id) }
    val preview = Character(data, Player(name.ifBlank { "?" }, raceId, classId))

    Column(
        Modifier
            .fillMaxSize()
            .background(Black)
            .systemBarsPadding()
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
    ) {
        Caps("Création du personnage", color = Red)
        Spacer(Modifier.height(16.dp))

        Row(verticalAlignment = Alignment.CenterVertically) {
            DotGrid(
                data.portrait(preview.race.portrait),
                Modifier
                    .width(120.dp)
                    .border(1.dp, Line, RoundedCornerShape(20.dp))
                    .padding(10.dp),
            )
            Column(Modifier.padding(start = 16.dp).weight(1f)) {
                Caps("Nom")
                Spacer(Modifier.height(6.dp))
                BasicTextField(
                    value = name,
                    onValueChange = { if (it.length <= 20) name = it },
                    singleLine = true,
                    textStyle = style(size = 20.sp),
                    cursorBrush = SolidColor(Red),
                    keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Words),
                    modifier = Modifier
                        .fillMaxWidth()
                        .border(1.dp, Line, RoundedCornerShape(12.dp))
                        .padding(12.dp),
                    decorationBox = { inner ->
                        Box {
                            if (name.isEmpty()) BasicText("Ton nom…", style = style(Gray, 20.sp))
                            inner()
                        }
                    },
                )
                Spacer(Modifier.height(8.dp))
                BasicText("${preview.race.name} · ${preview.charClass.name}", style = style(Red, 13.sp))
            }
        }

        SectionLabel("Race")
        LazyRow(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            items(data.races, key = { it.id }) { race ->
                RaceCard(race, data.portrait(race.portrait), race.id == raceId) { raceId = race.id }
            }
        }
        Spacer(Modifier.height(10.dp))
        BasicText(preview.race.desc, style = style(size = 14.sp))
        Spacer(Modifier.height(4.dp))
        val bonus = preview.race.bonus.entries.joinToString(" · ") { (ab, v) ->
            val abName = data.abilities.firstOrNull { it.id == ab }?.name ?: ab
            "$abName ${signed(v)}"
        }
        BasicText(bonus, style = style(Gray, 12.sp))

        SectionLabel("Classe")
        data.classes.chunked(2).forEach { pair ->
            Row(Modifier.fillMaxWidth().padding(bottom = 10.dp), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                pair.forEach { cls ->
                    ClassCard(cls, cls.id == classId, Modifier.weight(1f)) { classId = cls.id }
                }
                if (pair.size == 1) Spacer(Modifier.weight(1f))
            }
        }
        BasicText(preview.charClass.desc, style = style(size = 14.sp))

        SectionLabel("Caractéristiques")
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            data.abilities.forEach { ab ->
                StatBox(ab.id, preview.score(ab.id), preview.modifier(ab.id), Modifier.weight(1f))
            }
        }

        SectionLabel("Compétences maîtrisées")
        val skills = data.skills.values.filter { preview.isProficient(it.id) }
            .joinToString(" · ") { "${it.name} ${signed(preview.skillBonus(it.id))}" }
        BasicText(skills, style = style(size = 14.sp, lineHeight = 22.sp))

        Spacer(Modifier.height(28.dp))
        NButton("Commencer l'aventure", Modifier.fillMaxWidth(), enabled = name.isNotBlank()) {
            controller.newGame(Player(name.trim(), raceId, classId))
        }
        Spacer(Modifier.height(12.dp))
        NButton("Retour", Modifier.fillMaxWidth(), primary = false) { controller.screen = Screen.TITLE }
    }
}

@Composable
private fun SectionLabel(text: String) {
    Spacer(Modifier.height(26.dp))
    Caps(text)
    Spacer(Modifier.height(10.dp))
}

@Composable
private fun RaceCard(race: Race, portrait: List<String>, selected: Boolean, onClick: () -> Unit) {
    Column(
        Modifier
            .width(92.dp)
            .border(if (selected) 2.dp else 1.dp, if (selected) Red else Line, RoundedCornerShape(16.dp))
            .clickable(onClick = onClick)
            .padding(8.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        DotGrid(portrait, Modifier.fillMaxWidth())
        Spacer(Modifier.height(6.dp))
        BasicText(
            race.name, style = style(if (selected) Ink else Gray, 11.sp, FontWeight.Bold, align = TextAlign.Center),
        )
    }
}

@Composable
private fun ClassCard(cls: CharClass, selected: Boolean, modifier: Modifier, onClick: () -> Unit) {
    Box(
        modifier
            .border(if (selected) 2.dp else 1.dp, if (selected) Red else Line, RoundedCornerShape(14.dp))
            .clickable(onClick = onClick)
            .padding(vertical = 14.dp, horizontal = 12.dp),
        contentAlignment = Alignment.Center,
    ) {
        BasicText(cls.name.uppercase(), style = style(if (selected) Ink else Gray, 13.sp, FontWeight.Bold, 1.sp))
    }
}

@Composable
private fun StatBox(id: String, score: Int, mod: Int, modifier: Modifier) {
    Column(
        modifier
            .border(1.dp, Line, RoundedCornerShape(12.dp))
            .padding(vertical = 10.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Caps(id, size = 10.sp)
        BasicText(signed(mod), style = style(Ink, 16.sp, FontWeight.Bold))
        BasicText("$score", style = style(Gray, 11.sp))
    }
}
