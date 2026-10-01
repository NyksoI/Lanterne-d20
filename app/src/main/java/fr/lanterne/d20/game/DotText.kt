package fr.lanterne.d20.game

import java.text.Normalizer

/**
 * Convertit un texte en grille de points (police 5x7 définie dans game.json).
 * Légende des grilles : '.' vide, '+' gris, '#' blanc, 'r' rouge.
 */
object DotText {
    fun rows(font: Map<Char, List<String>>, text: String, ink: Char = '#'): List<String> {
        val clean = Normalizer.normalize(text.uppercase(), Normalizer.Form.NFD)
            .replace(Regex("\\p{M}+"), "")
        val glyphs = clean.map { font[it] ?: font[' '] ?: List(7) { "..." } }
        if (glyphs.isEmpty()) return List(7) { "" }
        return List(7) { row ->
            glyphs.joinToString(".") { glyph ->
                glyph.getOrElse(row) { "" }.replace('#', ink)
            }
        }
    }
}
