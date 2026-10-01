package fr.lanterne.d20.widget

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.widget.RemoteViews
import fr.lanterne.d20.MainActivity
import fr.lanterne.d20.R
import fr.lanterne.d20.game.Character
import fr.lanterne.d20.game.Dice
import fr.lanterne.d20.game.DotText
import fr.lanterne.d20.game.GameData
import fr.lanterne.d20.game.SaveStore

/**
 * Widget d'écran d'accueil façon Nothing :
 * à gauche le PNJ de ta scène en cours (portrait dot-matrix), au milieu sa réplique,
 * à droite un d20 qu'on peut lancer directement depuis l'écran d'accueil.
 */
class PnjWidget : AppWidgetProvider() {

    override fun onUpdate(context: Context, manager: AppWidgetManager, appWidgetIds: IntArray) {
        appWidgetIds.forEach { update(context, manager, it) }
    }

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == ACTION_ROLL) {
            SaveStore.setWidgetRoll(context, Dice.d20())
            updateAll(context)
            return
        }
        super.onReceive(context, intent)
    }

    companion object {
        private const val ACTION_ROLL = "fr.lanterne.d20.widget.ROLL"

        fun updateAll(context: Context) {
            val manager = AppWidgetManager.getInstance(context) ?: return
            val ids = manager.getAppWidgetIds(ComponentName(context, PnjWidget::class.java))
            ids.forEach { update(context, manager, it) }
        }

        private fun update(context: Context, manager: AppWidgetManager, widgetId: Int) {
            val data = GameData.load(context)
            val save = SaveStore.load(context)
            val views = RemoteViews(context.packageName, R.layout.widget_pnj)

            if (save == null) {
                views.setImageViewBitmap(R.id.widget_portrait, dotBitmap(data.portrait("scene_lanterne"), 14, true))
                views.setTextViewText(R.id.widget_name, "LANTERNE D'AUBE")
                views.setTextViewText(R.id.widget_sub, "Aucune aventure en cours")
                views.setTextViewText(R.id.widget_line, "Touche pour créer ton personnage.")
            } else {
                val character = Character(data, save.player)
                val scene = data.scene(save.sceneId)
                val npc = scene.npc?.let { data.npcs[it] }
                val portrait = data.portrait(npc?.portrait ?: "scene_lanterne")
                views.setImageViewBitmap(R.id.widget_portrait, dotBitmap(portrait, 14, true))
                views.setTextViewText(R.id.widget_name, (npc?.name ?: "Port-Brume").uppercase())
                views.setTextViewText(
                    R.id.widget_sub,
                    npc?.let { "${it.race} · ${it.title}" } ?: "${save.player.name} · ${character.race.name}",
                )
                views.setTextViewText(R.id.widget_line, character.fill(scene.text))
            }

            // dé du widget
            val roll = SaveStore.widgetRoll(context)
            val ink = if (roll == 1) 'r' else '#'
            val shown = if (roll == 0) 20 else roll

            views.setImageViewBitmap(R.id.widget_dice, dotBitmap(DotText.rows(data.font, shown.toString(), ink), 10, false))
            views.setTextViewText(
                R.id.widget_dice_label,
                when (roll) {
                    20 -> "CRITIQUE"
                    1 -> "AÏE"
                    else -> "D20"
                },
            )

            // actions : toucher le widget ouvre l'app, toucher le dé lance un d20
            val openApp = PendingIntent.getActivity(
                context, 0,
                Intent(context, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK),
                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
            )
            views.setOnClickPendingIntent(R.id.widget_main, openApp)

            val rollIntent = PendingIntent.getBroadcast(
                context, 1,
                Intent(context, PnjWidget::class.java).setAction(ACTION_ROLL),
                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
            )
            views.setOnClickPendingIntent(R.id.widget_roll, rollIntent)

            manager.updateAppWidget(widgetId, views)
        }

        /** Dessine une grille de points dans un Bitmap (le widget ne peut pas utiliser Compose). */
        private fun dotBitmap(rows: List<String>, cell: Int, showEmpty: Boolean): Bitmap {
            val cols = rows.maxOfOrNull { it.length }?.coerceAtLeast(1) ?: 1
            val height = rows.size.coerceAtLeast(1)
            val bitmap = Bitmap.createBitmap(cols * cell, height * cell, Bitmap.Config.ARGB_8888)
            val canvas = Canvas(bitmap)
            val paint = Paint(Paint.ANTI_ALIAS_FLAG)
            val radius = cell * 0.39f
            rows.forEachIndexed { y, line ->
                for (x in 0 until cols) {
                    val color = when (line.getOrElse(x) { '.' }) {
                        '#' -> 0xFFFFFFFF.toInt()
                        '+' -> 0xFF6E6E6E.toInt()
                        'r' -> 0xFFD71921.toInt()
                        else -> if (showEmpty) 0xFF1E1E1E.toInt() else null
                    } ?: continue
                    paint.color = color
                    canvas.drawCircle((x + 0.5f) * cell, (y + 0.5f) * cell, radius, paint)
                }
            }
            return bitmap
        }
    }
}
