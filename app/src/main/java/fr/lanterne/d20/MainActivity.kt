package fr.lanterne.d20

import android.graphics.Color
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.Crossfade
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import fr.lanterne.d20.game.GameController
import fr.lanterne.d20.game.Screen
import fr.lanterne.d20.ui.Black
import fr.lanterne.d20.ui.CreationScreen
import fr.lanterne.d20.ui.PlayScreen
import fr.lanterne.d20.ui.TitleScreen

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.dark(Color.TRANSPARENT),
        )
        val controller = GameController(this)
        setContent { LanterneApp(controller) }
    }
}

@Composable
fun LanterneApp(controller: GameController) {
    BackHandler(enabled = controller.screen != Screen.TITLE) {
        controller.screen = Screen.TITLE
    }
    Box(Modifier.fillMaxSize().background(Black)) {
        Crossfade(targetState = controller.screen, label = "ecran") { screen ->
            when (screen) {
                Screen.TITLE -> TitleScreen(controller)
                Screen.CREATION -> CreationScreen(controller)
                Screen.PLAY -> PlayScreen(controller)
            }
        }
    }
}
