package fr.lanterne.d20.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicText
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.cos
import kotlin.math.min
import kotlin.math.sin

// ── Palette Nothing : noir profond, blanc, un seul rouge ──
val Black = Color(0xFF000000)
val Ink = Color(0xFFFFFFFF)
val Gray = Color(0xFF8A8A8A)
val Line = Color(0xFF2A2A2A)
val Skin = Color(0xFF6E6E6E)
val EmptyDot = Color(0xFF181818)
val Red = Color(0xFFD71921)

val Mono = FontFamily.Monospace

fun style(
    color: Color = Ink,
    size: TextUnit = 15.sp,
    weight: FontWeight = FontWeight.Normal,
    spacing: TextUnit = 0.sp,
    align: TextAlign = TextAlign.Start,
    lineHeight: TextUnit = TextUnit.Unspecified,
) = TextStyle(
    color = color, fontSize = size, fontWeight = weight, fontFamily = Mono,
    letterSpacing = spacing, textAlign = align, lineHeight = lineHeight,
)

/** Petit texte en capitales espacées, façon interface Nothing. */
@Composable
fun Caps(text: String, modifier: Modifier = Modifier, color: Color = Gray, size: TextUnit = 11.sp) {
    BasicText(text.uppercase(), modifier, style = style(color, size, FontWeight.Bold, 1.5.sp))
}

/**
 * Affiche une grille de points (portrait, texte dot-matrix…).
 * '#' blanc, '+' gris, 'r' rouge, '.' point éteint.
 */
@Composable
fun DotGrid(rows: List<String>, modifier: Modifier = Modifier, showEmpty: Boolean = true, dotScale: Float = 0.78f) {
    val cols = rows.maxOfOrNull { it.length } ?: 0
    if (cols == 0 || rows.isEmpty()) return
    Canvas(modifier.aspectRatio(cols.toFloat() / rows.size)) {
        val cell = min(size.width / cols, size.height / rows.size)
        val radius = cell * dotScale / 2f
        val ox = (size.width - cell * cols) / 2f
        val oy = (size.height - cell * rows.size) / 2f
        rows.forEachIndexed { y, line ->
            for (x in 0 until cols) {
                val color = when (line.getOrElse(x) { '.' }) {
                    '#' -> Ink
                    '+' -> Skin
                    'r' -> Red
                    else -> if (showEmpty) EmptyDot else null
                } ?: continue
                drawCircle(color, radius, Offset(ox + (x + 0.5f) * cell, oy + (y + 0.5f) * cell))
            }
        }
    }
}

/** Contour d'un d20 vu de face : hexagone et facettes. */
@Composable
fun D20Shape(modifier: Modifier = Modifier, color: Color = Line) {
    Canvas(modifier.aspectRatio(1f)) {
        val c = Offset(size.width / 2f, size.height / 2f)
        val r = min(size.width, size.height) / 2f * 0.96f
        fun pt(angleDeg: Double, radius: Float) = Offset(
            c.x + radius * cos(Math.toRadians(angleDeg)).toFloat(),
            c.y + radius * sin(Math.toRadians(angleDeg)).toFloat(),
        )
        val hex = listOf(-90.0, -30.0, 30.0, 90.0, 150.0, 210.0).map { pt(it, r) }
        val tri = listOf(-90.0, 30.0, 150.0).map { pt(it, r * 0.6f) }
        val stroke = Stroke(width = 2.dp.toPx(), join = StrokeJoin.Round)

        val outline = Path().apply {
            moveTo(hex[0].x, hex[0].y)
            hex.drop(1).forEach { lineTo(it.x, it.y) }
            close()
        }
        drawPath(outline, color, style = stroke)
        val inner = Path().apply {
            moveTo(tri[0].x, tri[0].y)
            lineTo(tri[1].x, tri[1].y)
            lineTo(tri[2].x, tri[2].y)
            close()
        }
        drawPath(inner, color, style = stroke)
        // facettes : chaque sommet du triangle rejoint trois sommets de l'hexagone
        val links = listOf(0 to listOf(0, 1, 5), 1 to listOf(1, 2, 3), 2 to listOf(3, 4, 5))
        links.forEach { (t, hs) -> hs.forEach { h -> drawLine(color, tri[t], hex[h], stroke.width) } }
    }
}

/** Bouton pilule. Plein (blanc) ou contour. */
@Composable
fun NButton(
    text: String,
    modifier: Modifier = Modifier,
    primary: Boolean = true,
    enabled: Boolean = true,
    onClick: () -> Unit,
) {
    val shape = RoundedCornerShape(50)
    val bg = when {
        !enabled -> Modifier.background(Line, shape)
        primary -> Modifier.background(Ink, shape)
        else -> Modifier.border(1.dp, Gray, shape)
    }
    Box(
        modifier
            .clip(shape)
            .then(bg)
            .clickable(enabled = enabled, onClick = onClick)
            .padding(horizontal = 22.dp, vertical = 15.dp),
        contentAlignment = Alignment.Center,
    ) {
        BasicText(
            text.uppercase(),
            style = style(
                color = if (primary && enabled) Black else if (enabled) Ink else Gray,
                size = 13.sp, weight = FontWeight.Bold, spacing = 1.5.sp, align = TextAlign.Center,
            ),
        )
    }
}

/** Points rouges d'inspiration. */
@Composable
fun InspirationDots(count: Int, modifier: Modifier = Modifier) {
    Row(modifier, verticalAlignment = Alignment.CenterVertically) {
        Caps("Insp.", color = Gray, size = 10.sp)
        Spacer(Modifier.width(6.dp))
        if (count <= 0) {
            Box(Modifier.size(8.dp).border(1.dp, Line, CircleShape))
        }
        repeat(count.coerceAtMost(5)) {
            Box(Modifier.padding(end = 3.dp).size(8.dp).clip(CircleShape).background(Red))
        }
    }
}
