"""
Генератор нативного Android-додатку «Д10 Світло» (Kotlin + Material 3 DayNight + WorkManager + Widget 4x1).
Запускається автоматично у GitHub Actions перед командою `gradle assembleDebug`.
"""

from pathlib import Path

ROOT = Path("android_build")


def write_file(rel_path: str, content: str) -> None:
    target = ROOT / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.lstrip("\n"), encoding="utf-8")


# ------------------------------------------------------------------------------
# 1. Gradle конфігурація
# ------------------------------------------------------------------------------

SETTINGS_GRADLE = r"""
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "D10Svitlo"
include(":app")
"""

ROOT_BUILD_GRADLE = r"""
plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
}
"""

GRADLE_PROPERTIES = r"""
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
"""

APP_BUILD_GRADLE = r"""
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "ua.dnipro.d10svitlo"
    compileSdk = 34

    defaultConfig {
        applicationId = "ua.dnipro.d10svitlo"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
    }

    buildTypes {
        debug {
            isMinifyEnabled = false
        }
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.work:work-runtime-ktx:2.9.1")
}
"""

# ------------------------------------------------------------------------------
# 2. AndroidManifest.xml та ресурси (іконка «Д10 ⚡», віджет 4x1 Glass, тема)
# ------------------------------------------------------------------------------

ANDROID_MANIFEST = r"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:label="Д10 Світло"
        android:supportsRtl="true"
        android:theme="@style/Theme.D10Svitlo">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <receiver
            android:name=".D10WidgetProvider"
            android:exported="true"
            android:label="Д10 Світло (4×1)">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
                <action android:name="ua.dnipro.d10svitlo.WIDGET_REFRESH" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/d10_widget_info" />
        </receiver>
    </application>
</manifest>
"""

THEMES_XML = r"""
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.D10Svitlo" parent="Theme.Material3.DayNight.NoActionBar">
        <item name="android:statusBarColor">#0F172A</item>
        <item name="android:navigationBarColor">#0F172A</item>
    </style>
</resources>
"""

THEMES_NIGHT_XML = r"""
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.D10Svitlo" parent="Theme.Material3.DayNight.NoActionBar">
        <item name="android:statusBarColor">#0F172A</item>
        <item name="android:navigationBarColor">#141B2D</item>
    </style>
</resources>
"""

# 10-В: Личный знак «Д10 ⚡» (Adaptive Icon)
IC_LAUNCHER_XML = r"""
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
"""

IC_LAUNCHER_BG = r"""
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#18181B"
        android:pathData="M0,0h108v108h-108z" />
    <path
        android:fillColor="#27272A"
        android:pathData="M0,0 L108,0 L108,58 C78,42 32,74 0,54 Z" />
</vector>
"""

IC_LAUNCHER_FG = r"""
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <!-- Золота блискавка зверху -->
    <path
        android:fillColor="#FACC15"
        android:pathData="M57,26 L45.5,40.5 L53,40.5 L50,50.5 L62.5,35.5 L55,35.5 Z" />
    <!-- Д -->
    <path
        android:pathData="M34.5,56.5 L44,56.5 L44,74 M34.5,56.5 C34.5,64 33.5,70 31.5,74 M29.5,74 L46.5,74 M29.5,74 L29.5,78 M46.5,74 L46.5,78"
        android:strokeWidth="3.6"
        android:strokeColor="#FFFFFF"
        android:strokeLineCap="round"
        android:strokeLineJoin="round" />
    <!-- 1 -->
    <path
        android:pathData="M53,60.5 L57.5,56.5 L57.5,76 M53.5,76 L61.5,76"
        android:strokeWidth="3.6"
        android:strokeColor="#FFFFFF"
        android:strokeLineCap="round"
        android:strokeLineJoin="round" />
    <!-- 0 -->
    <path
        android:pathData="M73,56.5 C76.8,56.5 79,59.5 79,66.25 C79,73 76.8,76 73,76 C69.2,76 67,73 67,66.25 C67,59.5 69.2,56.5 73,56.5 Z"
        android:strokeWidth="3.6"
        android:strokeColor="#FFFFFF"
        android:strokeLineCap="round"
        android:strokeLineJoin="round" />
</vector>
"""

IC_NOTIF_BOLT = r"""
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M13,2 L4,14 L11,14 L10,22 L20,10 L13,10 Z" />
</vector>
"""

# 9-Б: Напівпрозорий віджет 4x1 (Glass)
WIDGET_INFO_XML = r"""
<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="250dp"
    android:minHeight="48dp"
    android:targetCellWidth="4"
    android:targetCellHeight="1"
    android:resizeMode="horizontal"
    android:updatePeriodMillis="1800000"
    android:initialLayout="@layout/widget_d10"
    android:widgetCategory="home_screen" />
"""

WIDGET_GLASS_BG = r"""
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#8C0F172A" />
    <corners android:radius="18dp" />
    <stroke android:width="1dp" android:color="#40FFFFFF" />
</shape>
"""

WIDGET_BAR_MINT = r"""
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#2A9D8F" />
    <corners android:radius="4dp" />
</shape>
"""

WIDGET_BAR_OCHRE = r"""
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#D4A348" />
    <corners android:radius="4dp" />
</shape>
"""

WIDGET_BAR_TERRACOTTA = r"""
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#C85555" />
    <corners android:radius="4dp" />
</shape>
"""

WIDGET_LAYOUT_XML = r"""
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/widget_root"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@drawable/widget_glass_bg"
    android:gravity="center_vertical"
    android:orientation="horizontal"
    android:paddingStart="12dp"
    android:paddingEnd="10dp"
    android:paddingTop="8dp"
    android:paddingBottom="8dp">

    <ImageView
        android:id="@+id/widget_bar"
        android:layout_width="5dp"
        android:layout_height="34dp"
        android:contentDescription="status"
        android:src="@drawable/widget_bar_mint" />

    <LinearLayout
        android:id="@+id/widget_text_box"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginStart="10dp"
        android:layout_marginEnd="8dp"
        android:layout_weight="1"
        android:orientation="vertical">

        <TextView
            android:id="@+id/widget_title"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:ellipsize="end"
            android:maxLines="1"
            android:text="Д10 Світло"
            android:textColor="#FFFFFF"
            android:textSize="13sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/widget_subtitle"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="1dp"
            android:ellipsize="end"
            android:maxLines="1"
            android:text="Натисніть для оновлення"
            android:textColor="#D9E2EC"
            android:textSize="11sp" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/widget_refresh_btn"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:orientation="vertical"
        android:padding="4dp">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="↻"
            android:textColor="#FFFFFF"
            android:textSize="17sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/widget_time"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="--:--"
            android:textColor="#CBD5E1"
            android:textSize="9sp" />
    </LinearLayout>
</LinearLayout>
"""

# ------------------------------------------------------------------------------
# 3. Kotlin вихідний код: ModelsAndStore.kt
# ------------------------------------------------------------------------------

MODELS_AND_STORE_KT = r"""
package ua.dnipro.d10svitlo

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.time.Duration
import java.time.Instant
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.OffsetDateTime
import java.time.ZoneId
import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter

object AppConfig {
    const val DEFAULT_STATE_URL =
        "https://raw.githubusercontent.com/MaClaDoff/dtek-bot/bot-state/state.json"
    const val ADDRESS_SHORT = "м. Дніпро, пров. Добровольців, 10"
    val KYIV_ZONE: ZoneId = ZoneId.of("Europe/Kyiv")
    const val MAX_HISTORY_ITEMS = 20
}

data class BannerInfo(
    val active: Boolean = false,
    val reason: String = "",
    val startDate: String = "",
    val endDate: String = "",
    val outageType: String = "",
    val updateTimestamp: String = ""
)

data class DaySchedule(
    val dateIso: String,
    val dateLabel: String,
    val intervals: List<Pair<String, String>>,
    val possibleIntervals: List<Pair<String, String>>
)

data class DtekState(
    val groupId: String = "",
    val banner: BannerInfo = BannerInfo(),
    val endDateHistory: List<String> = emptyList(),
    val schedules: Map<String, DaySchedule> = emptyMap(),
    val lastSuccessfulCheck: String = ""
)

/** status: 0 = світло є (Mint), 1 = відключення (Terracotta), 2 = можливе (Ochre) */
data class TimelineSegment(
    val startMin: Int,
    val endMin: Int,
    val status: Int
)

data class HistoryEvent(
    val epochMs: Long,
    val timeLabel: String,
    val icon: String,
    val title: String,
    val subtitle: String
)

data class AppSettings(
    val notificationsEnabled: Boolean = true,
    val quietEnabled: Boolean = true,
    val quietStartHour: Int = 23,
    val quietEndHour: Int = 7,
    val quietSilentOnly: Boolean = true,
    val stateUrl: String = AppConfig.DEFAULT_STATE_URL
)

data class TrafficLightStatus(
    val level: Int, // 0 = Mint, 1 = Ochre, 2 = Terracotta
    val title: String,
    val subtitle: String
)

object DtekParser {
    private val dtekFormats = listOf(
        DateTimeFormatter.ofPattern("HH:mm dd.MM.yyyy"),
        DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm"),
        DateTimeFormatter.ofPattern("HH:mm dd.MM.yy"),
        DateTimeFormatter.ofPattern("dd.MM.yy HH:mm")
    )

    fun nowKyiv(): ZonedDateTime = ZonedDateTime.now(AppConfig.KYIV_ZONE)

    fun parseState(jsonStr: String): DtekState? {
        return try {
            val root = JSONObject(jsonStr)
            val bObj = root.optJSONObject("banner") ?: JSONObject()
            val banner = BannerInfo(
                active = bObj.optBoolean("active", false),
                reason = bObj.optString("reason", "").trim(),
                startDate = bObj.optString("start_date", "").trim(),
                endDate = bObj.optString("end_date", "").trim(),
                outageType = bObj.optString("outage_type", "").trim(),
                updateTimestamp = bObj.optString("update_timestamp", "").trim()
            )

            val historyArr = root.optJSONArray("end_date_history")
            val historyList = mutableListOf<String>()
            if (historyArr != null) {
                for (i in 0 until historyArr.length()) {
                    val item = historyArr.optString(i, "").trim()
                    if (item.isNotEmpty()) historyList.add(item)
                }
            }

            val schedulesMap = linkedMapOf<String, DaySchedule>()
            val sObj = root.optJSONObject("schedules")
            if (sObj != null) {
                val keys = sObj.keys()
                while (keys.hasNext()) {
                    val k = keys.next()
                    val dObj = sObj.optJSONObject(k) ?: continue
                    val dateIso = dObj.optString("date_iso", k)
                    val dateLabel = dObj.optString("date_label", k)
                    val intervals = parseIntervalArray(dObj.optJSONArray("intervals"))
                    val possible = parseIntervalArray(dObj.optJSONArray("possible_intervals"))
                    schedulesMap[dateIso] = DaySchedule(dateIso, dateLabel, intervals, possible)
                }
            }

            DtekState(
                groupId = root.optString("group_id", "").trim(),
                banner = banner,
                endDateHistory = historyList,
                schedules = schedulesMap,
                lastSuccessfulCheck = root.optString("last_successful_check", "").trim()
            )
        } catch (_: Exception) {
            null
        }
    }

    private fun parseIntervalArray(arr: JSONArray?): List<Pair<String, String>> {
        val result = mutableListOf<Pair<String, String>>()
        if (arr == null) return result
        for (i in 0 until arr.length()) {
            val pair = arr.optJSONArray(i) ?: continue
            if (pair.length() >= 2) {
                val s = pair.optString(0, "").trim()
                val e = pair.optString(1, "").trim()
                if (s.isNotEmpty() && e.isNotEmpty()) {
                    result.add(Pair(s, e))
                }
            }
        }
        return result
    }

    fun formatGroupPretty(groupId: String): String {
        if (groupId.isBlank()) return ""
        return "Черга ${groupId.replace("GPV", "")}"
    }

    fun shortEndTime(raw: String): String {
        val cleaned = raw.trim().removePrefix("до ").trim()
        val parts = cleaned.split(" ")
        return parts.firstOrNull()?.takeIf { it.contains(":") } ?: cleaned
    }

    fun parseDtekDateTime(raw: String): LocalDateTime? {
        val cleaned = raw.trim().replace(Regex("^до\\s+", RegexOption.IGNORE_CASE), "").trim()
        if (cleaned.isEmpty()) return null
        for (fmt in dtekFormats) {
            try {
                return LocalDateTime.parse(cleaned, fmt)
            } catch (_: Exception) {
            }
        }
        return null
    }

    fun formatDeltaUa(oldDt: LocalDateTime, newDt: LocalDateTime): String {
        val diffMin = Duration.between(oldDt, newDt).toMinutes()
        if (diffMin == 0L) return "без змін"
        val sign = if (diffMin > 0) "+" else "-"
        val absMin = kotlin.math.abs(diffMin)
        val days = absMin / (24 * 60)
        val rem = absMin % (24 * 60)
        val hours = rem / 60
        val mins = rem % 60
        val parts = mutableListOf<String>()
        if (days > 0) parts.add("${days} дн")
        if (hours > 0) parts.add("${hours} год")
        if (mins > 0 || parts.isEmpty()) parts.add("${mins} хв")
        return "$sign${parts.joinToString(" ")}"
    }

    fun timeToMinutes(hhmm: String): Int {
        val parts = hhmm.trim().split(":")
        if (parts.size < 2) return 0
        val h = parts[0].toIntOrNull() ?: 0
        val m = parts[1].toIntOrNull() ?: 0
        return (h * 60 + m).coerceIn(0, 1440)
    }

    fun minutesToHHMM(min: Int): String {
        val clamped = min.coerceIn(0, 1440)
        val h = clamped / 60
        val m = clamped % 60
        return String.format("%02d:%02d", h, m)
    }

    fun formatDurationUa(totalMinutes: Int): String {
        val h = totalMinutes / 60
        val m = totalMinutes % 60
        return when {
            h > 0 && m > 0 -> "$h год $m хв"
            h > 0 -> "$h год"
            else -> "$m хв"
        }
    }

    fun buildHalfHourSlots(day: DaySchedule?): IntArray {
        val slots = IntArray(48) { 0 }
        if (day == null) return slots
        for ((s, e) in day.possibleIntervals) {
            val sIdx = (timeToMinutes(s) / 30).coerceIn(0, 48)
            val eIdx = (timeToMinutes(e) / 30).coerceIn(0, 48)
            for (i in sIdx until eIdx) slots[i] = 2
        }
        for ((s, e) in day.intervals) {
            val sIdx = (timeToMinutes(s) / 30).coerceIn(0, 48)
            val eIdx = (timeToMinutes(e) / 30).coerceIn(0, 48)
            for (i in sIdx until eIdx) slots[i] = 1
        }
        return slots
    }

    fun buildTimelineSegments(day: DaySchedule?): List<TimelineSegment> {
        val slots = buildHalfHourSlots(day)
        val result = mutableListOf<TimelineSegment>()
        var curStatus = slots[0]
        var startIdx = 0
        for (i in 1 until 48) {
            if (slots[i] != curStatus) {
                result.add(TimelineSegment(startIdx * 30, i * 30, curStatus))
                curStatus = slots[i]
                startIdx = i
            }
        }
        result.add(TimelineSegment(startIdx * 30, 1440, curStatus))
        return result
    }

    fun minutesSinceServerCheck(state: DtekState?): Long? {
        val raw = state?.lastSuccessfulCheck ?: return null
        if (raw.isBlank()) return null
        return try {
            val instant = OffsetDateTime.parse(raw).toInstant()
            Duration.between(instant, Instant.now()).toMinutes().coerceAtLeast(0)
        } catch (_: Exception) {
            null
        }
    }

    fun computeTrafficLight(state: DtekState?): TrafficLightStatus {
        if (state == null) {
            return TrafficLightStatus(1, "Немає даних", "Натисніть ↻ для завантаження")
        }

        if (state.banner.active) {
            val endTxt = if (state.banner.endDate.isNotEmpty()) {
                "до ${shortEndTime(state.banner.endDate)}"
            } else {
                "час уточнюється"
            }
            val reason = state.banner.reason.ifBlank { "Відсутня електроенергія" }
            return TrafficLightStatus(2, "Аварія • $endTxt", reason)
        }

        val now = nowKyiv()
        val todayIso = now.toLocalDate().toString()
        val nowMin = now.hour * 60 + now.minute
        val today = state.schedules[todayIso]
        val groupTxt = formatGroupPretty(state.groupId)

        if (today != null) {
            val segments = buildTimelineSegments(today)
            val currentSeg = segments.firstOrNull { nowMin in it.startMin until it.endMin }
            if (currentSeg != null && currentSeg.status == 1) {
                val endStr = minutesToHHMM(currentSeg.endMin)
                return TrafficLightStatus(
                    2,
                    "Планове вимкнення до $endStr",
                    "За графіком ГПВ${if (groupTxt.isNotEmpty()) " • $groupTxt" else ""}"
                )
            }
            if (currentSeg != null && currentSeg.status == 2) {
                val endStr = minutesToHHMM(currentSeg.endMin)
                return TrafficLightStatus(
                    1,
                    "Можливе вимкнення до $endStr",
                    "Сіра зона графіка${if (groupTxt.isNotEmpty()) " • $groupTxt" else ""}"
                )
            }

            // Шукаємо найближче відключення сьогодні
            val nextOff = today.intervals
                .map { Pair(timeToMinutes(it.first), it) }
                .filter { it.first > nowMin }
                .minByOrNull { it.first }

            if (nextOff != null) {
                val minsUntil = nextOff.first - nowMin
                val rangeStr = "${nextOff.second.first} — ${nextOff.second.second}"
                return if (minsUntil <= 35) {
                    TrafficLightStatus(
                        1,
                        "Скоро вимкнення о ${nextOff.second.first}",
                        "Заплановано: $rangeStr"
                    )
                } else {
                    TrafficLightStatus(
                        0,
                        "Світло за графіком",
                        "Наступне: $rangeStr"
                    )
                }
            }
        }

        val tomorrowIso = now.toLocalDate().plusDays(1).toString()
        val tomorrow = state.schedules[tomorrowIso]
        val tomorrowFirst = tomorrow?.intervals?.firstOrNull()
        val sub = when {
            tomorrowFirst != null -> "Завтра з ${tomorrowFirst.first} — ${tomorrowFirst.second}"
            today != null -> "Сьогодні вимкнень більше немає"
            else -> AppConfig.ADDRESS_SHORT
        }
        return TrafficLightStatus(0, "Світло за графіком", sub)
    }

    fun formatCompactIntervals(day: DaySchedule): String {
        if (day.intervals.isEmpty() && day.possibleIntervals.isEmpty()) {
            return "Відключень не заплановано"
        }
        val parts = mutableListOf<String>()
        for ((s, e) in day.intervals) parts.add("$s–$e")
        for ((s, e) in day.possibleIntervals) parts.add("$s–$e (можл.)")
        return parts.joinToString(", ")
    }

    fun buildShareText(state: DtekState?): String {
        val sb = StringBuilder()
        sb.append("⚡ Д10 Світло • ${AppConfig.ADDRESS_SHORT}\n")
        if (state == null) {
            sb.append("Дані ще не завантажено.")
            return sb.toString()
        }
        val group = formatGroupPretty(state.groupId)
        if (group.isNotEmpty()) sb.append("🔢 $group\n")
        sb.append("\n")

        if (state.banner.active) {
            sb.append("🚨 ${state.banner.reason.ifBlank { "Відсутня електроенергія" }}\n")
            if (state.banner.startDate.isNotEmpty()) sb.append("🕒 Початок: ${state.banner.startDate}\n")
            if (state.banner.endDate.isNotEmpty()) sb.append("🔌 Відновлення: до ${state.banner.endDate}\n")
            sb.append("\n")
        } else {
            sb.append("🟢 Активних аварій на сайті ДТЕК немає\n\n")
        }

        val todayIso = nowKyiv().toLocalDate().toString()
        val tomorrowIso = nowKyiv().toLocalDate().plusDays(1).toString()

        state.schedules[todayIso]?.let { d ->
            sb.append("📅 Сьогодні (${d.dateLabel}):\n")
            sb.append(formatShareDayLines(d)).append("\n")
        }
        state.schedules[tomorrowIso]?.let { d ->
            sb.append("🔮 Завтра (${d.dateLabel}):\n")
            sb.append(formatShareDayLines(d)).append("\n")
        }
        return sb.toString().trim()
    }

    private fun formatShareDayLines(day: DaySchedule): String {
        if (day.intervals.isEmpty() && day.possibleIntervals.isEmpty()) {
            return "  • Відключень не заплановано\n"
        }
        val sb = StringBuilder()
        for ((s, e) in day.intervals) sb.append("  • 🪫 $s — $e\n")
        for ((s, e) in day.possibleIntervals) sb.append("  • 🟡 $s — $e (можливе)\n")
        return sb.toString()
    }
}

class AppStore(context: Context) {
    private val prefs = context.getSharedPreferences("d10_svitlo_prefs", Context.MODE_PRIVATE)

    fun getSettings(): AppSettings = AppSettings(
        notificationsEnabled = prefs.getBoolean("notif_enabled", true),
        quietEnabled = prefs.getBoolean("quiet_enabled", true),
        quietStartHour = prefs.getInt("quiet_start", 23),
        quietEndHour = prefs.getInt("quiet_end", 7),
        quietSilentOnly = prefs.getBoolean("quiet_silent_only", true),
        stateUrl = prefs.getString("state_url", AppConfig.DEFAULT_STATE_URL)
            ?.takeIf { it.isNotBlank() } ?: AppConfig.DEFAULT_STATE_URL
    )

    fun saveSettings(s: AppSettings) {
        prefs.edit()
            .putBoolean("notif_enabled", s.notificationsEnabled)
            .putBoolean("quiet_enabled", s.quietEnabled)
            .putInt("quiet_start", s.quietStartHour.coerceIn(0, 23))
            .putInt("quiet_end", s.quietEndHour.coerceIn(0, 23))
            .putBoolean("quiet_silent_only", s.quietSilentOnly)
            .putString("state_url", s.stateUrl.trim().ifEmpty { AppConfig.DEFAULT_STATE_URL })
            .apply()
    }

    fun getCachedStateJson(): String? = prefs.getString("cached_state_json", null)

    fun getCachedState(): DtekState? = getCachedStateJson()?.let { DtekParser.parseState(it) }

    fun saveCachedState(json: String, syncEpochMs: Long) {
        prefs.edit()
            .putString("cached_state_json", json)
            .putLong("last_sync_epoch_ms", syncEpochMs)
            .apply()
    }

    fun getLastSyncEpochMs(): Long = prefs.getLong("last_sync_epoch_ms", 0L)

    fun isInitialized(): Boolean = prefs.getBoolean("sync_initialized", false)

    fun setInitialized() {
        prefs.edit().putBoolean("sync_initialized", true).apply()
    }

    fun getPrevBanner(): BannerInfo = BannerInfo(
        active = prefs.getBoolean("prev_b_active", false),
        reason = prefs.getString("prev_b_reason", "") ?: "",
        startDate = prefs.getString("prev_b_start", "") ?: "",
        endDate = prefs.getString("prev_b_end", "") ?: ""
    )

    fun savePrevBanner(b: BannerInfo) {
        prefs.edit()
            .putBoolean("prev_b_active", b.active)
            .putString("prev_b_reason", b.reason)
            .putString("prev_b_start", b.startDate)
            .putString("prev_b_end", b.endDate)
            .apply()
    }

    fun getPrevSchedulesMap(): Map<String, String> {
        val raw = prefs.getString("prev_schedules_map", null) ?: return emptyMap()
        return try {
            val obj = JSONObject(raw)
            val map = mutableMapOf<String, String>()
            val keys = obj.keys()
            while (keys.hasNext()) {
                val k = keys.next()
                map[k] = obj.optString(k, "")
            }
            map
        } catch (_: Exception) {
            emptyMap()
        }
    }

    fun savePrevSchedulesMap(map: Map<String, String>) {
        val obj = JSONObject()
        for ((k, v) in map) obj.put(k, v)
        prefs.edit().putString("prev_schedules_map", obj.toString()).apply()
    }

    fun getWarnedKeys(): MutableSet<String> {
        val set = prefs.getStringSet("warned_keys", emptySet()) ?: emptySet()
        return set.toMutableSet()
    }

    fun saveWarnedKeys(keys: Set<String>) {
        prefs.edit().putStringSet("warned_keys", keys.toSet()).apply()
    }

    fun getHistory(): List<HistoryEvent> {
        val raw = prefs.getString("event_history", null) ?: return emptyList()
        return try {
            val arr = JSONArray(raw)
            val list = mutableListOf<HistoryEvent>()
            for (i in 0 until arr.length()) {
                val o = arr.optJSONObject(i) ?: continue
                list.add(
                    HistoryEvent(
                        epochMs = o.optLong("ts", 0L),
                        timeLabel = o.optString("label", ""),
                        icon = o.optString("icon", "•"),
                        title = o.optString("title", ""),
                        subtitle = o.optString("sub", "")
                    )
                )
            }
            list
        } catch (_: Exception) {
            emptyList()
        }
    }

    fun addHistoryEvent(icon: String, title: String, subtitle: String) {
        val now = DtekParser.nowKyiv()
        val label = now.format(DateTimeFormatter.ofPattern("dd.MM HH:mm"))
        val current = getHistory().toMutableList()
        current.add(0, HistoryEvent(System.currentTimeMillis(), label, icon, title, subtitle))
        val trimmed = current.take(AppConfig.MAX_HISTORY_ITEMS)
        val arr = JSONArray()
        for (ev in trimmed) {
            arr.put(
                JSONObject()
                    .put("ts", ev.epochMs)
                    .put("label", ev.timeLabel)
                    .put("icon", ev.icon)
                    .put("title", ev.title)
                    .put("sub", ev.subtitle)
            )
        }
        prefs.edit().putString("event_history", arr.toString()).apply()
    }

    fun clearHistory() {
        prefs.edit().remove("event_history").apply()
    }
}
"""

# ------------------------------------------------------------------------------
# 4. Kotlin: NotificationHelper.kt (11-А ультра-короткі + 6-Г тихі години)
# ------------------------------------------------------------------------------

NOTIFICATION_HELPER_KT = r"""
package ua.dnipro.d10svitlo

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat

object NotificationHelper {
    private const val CHANNEL_LOUD = "d10_alerts_loud"
    private const val CHANNEL_SILENT = "d10_alerts_silent"

    fun ensureChannels(context: Context) {
        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        val loud = NotificationChannel(
            CHANNEL_LOUD,
            "Сповіщення Д10 (зі звуком)",
            NotificationManager.IMPORTANCE_HIGH
        ).apply {
            description = "Аварії, переноси, оновлення графіків та попередження"
        }

        val silent = NotificationChannel(
            CHANNEL_SILENT,
            "Тихі сповіщення Д10 (ніч)",
            NotificationManager.IMPORTANCE_LOW
        ).apply {
            description = "Без звуку та вібрації у тихі години"
            setSound(null, null)
            enableVibration(false)
        }

        manager.createNotificationChannel(loud)
        manager.createNotificationChannel(silent)
    }

    fun isQuietHoursNow(settings: AppSettings): Boolean {
        if (!settings.quietEnabled) return false
        val hour = DtekParser.nowKyiv().hour
        val start = settings.quietStartHour
        val end = settings.quietEndHour
        return if (start > end) {
            hour >= start || hour < end
        } else if (start < end) {
            hour in start until end
        } else {
            false
        }
    }

    fun hasPermission(context: Context): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            ContextCompat.checkSelfPermission(
                context,
                Manifest.permission.POST_NOTIFICATIONS
            ) == PackageManager.PERMISSION_GRANTED
        } else {
            true
        }
    }

    fun sendShortAlert(
        context: Context,
        title: String,
        body: String,
        isTest: Boolean = false
    ) {
        ensureChannels(context)
        if (!hasPermission(context)) return

        val settings = AppStore(context).getSettings()
        if (!isTest && !settings.notificationsEnabled) return

        val quietNow = !isTest && isQuietHoursNow(settings)
        if (quietNow && !settings.quietSilentOnly) {
            // Користувач обрав повністю не турбувати вночі
            return
        }

        val channelId = if (quietNow) CHANNEL_SILENT else CHANNEL_LOUD
        val priority = if (quietNow) NotificationCompat.PRIORITY_LOW else NotificationCompat.PRIORITY_HIGH

        val openIntent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        val pi = PendingIntent.getActivity(
            context,
            0,
            openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val builder = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(R.drawable.ic_notif_bolt)
            .setContentTitle(title)
            .setContentText(body)
            .setPriority(priority)
            .setContentIntent(pi)
            .setAutoCancel(true)
            .setSilent(quietNow)

        val notifId = ((System.currentTimeMillis() % 100000) + title.hashCode()).toInt()
        try {
            NotificationManagerCompat.from(context).notify(notifId, builder.build())
        } catch (_: SecurityException) {
        }
    }
}
"""

# ------------------------------------------------------------------------------
# 5. Kotlin: DtekSyncManager.kt (WorkManager кожні 30 хв + точне попередження)
# ------------------------------------------------------------------------------

SYNC_MANAGER_KT = r"""
package ua.dnipro.d10svitlo

import android.content.Context
import androidx.work.Constraints
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.ExistingWorkPolicy
import androidx.work.NetworkType
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.Worker
import androidx.work.WorkerParameters
import java.net.HttpURLConnection
import java.net.URL
import java.time.Duration
import java.time.LocalDate
import java.time.ZonedDateTime
import java.util.concurrent.TimeUnit

data class SyncResult(
    val ok: Boolean,
    val state: DtekState?,
    val errorMsg: String? = null
)

object DtekSyncManager {
    private const val PERIODIC_WORK_NAME = "d10_periodic_sync_30m"
    private const val PRE_WARN_WORK_NAME = "d10_pre_outage_warn"

    fun schedulePeriodicSync(context: Context) {
        val constraints = Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .build()

        val request = PeriodicWorkRequestBuilder<DtekSyncWorker>(30, TimeUnit.MINUTES)
            .setConstraints(constraints)
            .build()

        WorkManager.getInstance(context).enqueueUniquePeriodicWork(
            PERIODIC_WORK_NAME,
            ExistingPeriodicWorkPolicy.KEEP,
            request
        )
    }

    fun triggerImmediateSync(context: Context) {
        val req = OneTimeWorkRequestBuilder<DtekSyncWorker>().build()
        WorkManager.getInstance(context).enqueue(req)
    }

    fun fetchAndProcess(context: Context): SyncResult {
        val store = AppStore(context)
        val settings = store.getSettings()

        val rawJson = try {
            downloadStateJson(settings.stateUrl)
        } catch (e: Exception) {
            return SyncResult(false, store.getCachedState(), e.message ?: "Немає з'єднання")
        }

        val state = DtekParser.parseState(rawJson)
            ?: return SyncResult(false, store.getCachedState(), "Некоректний формат state.json")

        store.saveCachedState(rawJson, System.currentTimeMillis())

        val todayIso = DtekParser.nowKyiv().toLocalDate().toString()
        val tomorrowIso = DtekParser.nowKyiv().toLocalDate().plusDays(1).toString()

        val currentSchedSig = mutableMapOf<String, String>()
        for ((k, d) in state.schedules) {
            currentSchedSig[k] = DtekParser.formatCompactIntervals(d)
        }

        if (!store.isInitialized()) {
            store.savePrevBanner(state.banner)
            store.savePrevSchedulesMap(currentSchedSig)
            store.setInitialized()
            store.addHistoryEvent(
                "⚡",
                "Додаток підключено",
                DtekParser.computeTrafficLight(state).title
            )
        } else {
            processBannerDiff(context, store, state)
            processScheduleDiff(context, store, state, currentSchedSig, todayIso, tomorrowIso)
            processPreOutageWarning(context, store, state, todayIso, tomorrowIso)
        }

        scheduleNextPreOutageCheck(context, state, todayIso, tomorrowIso)
        D10WidgetProvider.updateAllWidgets(context)
        return SyncResult(true, state, null)
    }

    private fun downloadStateJson(baseUrl: String): String {
        val sep = if (baseUrl.contains("?")) "&" else "?"
        val url = URL("${baseUrl}${sep}t=${System.currentTimeMillis()}")
        val conn = (url.openConnection() as HttpURLConnection).apply {
            requestMethod = "GET"
            connectTimeout = 12_000
            readTimeout = 12_000
            useCaches = false
            setRequestProperty("Cache-Control", "no-cache")
            setRequestProperty("User-Agent", "D10SvitloAndroid/1.0")
        }
        try {
            val code = conn.responseCode
            if (code !in 200..299) {
                throw RuntimeException("HTTP $code")
            }
            return conn.inputStream.bufferedReader(Charsets.UTF_8).use { it.readText() }
        } finally {
            conn.disconnect()
        }
    }

    private fun processBannerDiff(context: Context, store: AppStore, state: DtekState) {
        val prev = store.getPrevBanner()
        val curr = state.banner

        if (curr.active && !prev.active) {
            val endShort = DtekParser.shortEndTime(curr.endDate)
            val title = if (endShort.isNotEmpty()) {
                "🚨 Відсутнє світло • до $endShort"
            } else {
                "🚨 Відсутня електроенергія"
            }
            val body = curr.reason.ifBlank { AppConfig.ADDRESS_SHORT }
            NotificationHelper.sendShortAlert(context, title, body)
            store.addHistoryEvent("🚨", title, body)
        } else if (curr.active && prev.active) {
            val meaningfulChanged =
                prev.reason != curr.reason ||
                    prev.startDate != curr.startDate ||
                    prev.endDate != curr.endDate

            if (meaningfulChanged) {
                if (prev.endDate != curr.endDate && curr.endDate.isNotEmpty()) {
                    val oldDt = DtekParser.parseDtekDateTime(prev.endDate)
                    val newDt = DtekParser.parseDtekDateTime(curr.endDate)
                    val delta = if (oldDt != null && newDt != null) {
                        " (${DtekParser.formatDeltaUa(oldDt, newDt)})"
                    } else {
                        ""
                    }
                    val endShort = DtekParser.shortEndTime(curr.endDate)
                    val title = "🔄 Перенос: до $endShort$delta"
                    val body = curr.reason.ifBlank { "Оновлено час відновлення" }
                    NotificationHelper.sendShortAlert(context, title, body)
                    store.addHistoryEvent("🔄", title, body)
                } else {
                    val title = "🔄 Оновлення відключення"
                    val endShort = DtekParser.shortEndTime(curr.endDate)
                    val body = listOfNotNull(
                        curr.reason.takeIf { it.isNotBlank() },
                        endShort.takeIf { it.isNotBlank() }?.let { "до $it" }
                    ).joinToString(" • ")
                    NotificationHelper.sendShortAlert(context, title, body)
                    store.addHistoryEvent("🔄", title, body)
                }
            }
        } else if (!curr.active && prev.active) {
            val title = "✅ Відключення знято"
            val body = "Світло за графіком • пров. Добровольців, 10"
            NotificationHelper.sendShortAlert(context, title, body)
            store.addHistoryEvent("✅", title, body)
        }

        store.savePrevBanner(curr)
    }

    private fun processScheduleDiff(
        context: Context,
        store: AppStore,
        state: DtekState,
        currentSig: Map<String, String>,
        todayIso: String,
        tomorrowIso: String
    ) {
        val prevSig = store.getPrevSchedulesMap()

        val todayChanged = currentSig[todayIso] != null && currentSig[todayIso] != prevSig[todayIso]
        val tomorrowChanged = currentSig[tomorrowIso] != null && currentSig[tomorrowIso] != prevSig[tomorrowIso]

        if (tomorrowChanged) {
            val day = state.schedules[tomorrowIso]
            if (day != null) {
                val title = "🔮 Графік на завтра (${day.dateLabel})"
                val body = DtekParser.formatCompactIntervals(day)
                NotificationHelper.sendShortAlert(context, title, body)
                store.addHistoryEvent("🔮", title, body)
            }
        }
        if (todayChanged) {
            val day = state.schedules[todayIso]
            if (day != null) {
                val title = "📅 Оновився графік на сьогодні"
                val body = DtekParser.formatCompactIntervals(day)
                NotificationHelper.sendShortAlert(context, title, body)
                store.addHistoryEvent("📅", title, body)
            }
        }

        store.savePrevSchedulesMap(currentSig)
    }

    private fun processPreOutageWarning(
        context: Context,
        store: AppStore,
        state: DtekState,
        todayIso: String,
        tomorrowIso: String
    ) {
        if (state.banner.active) return

        val now = DtekParser.nowKyiv()
        val warned = store.getWarnedKeys()
            .filter { it.startsWith(todayIso) || it.startsWith(tomorrowIso) }
            .toMutableSet()

        for (dateIso in listOf(todayIso, tomorrowIso)) {
            val day = state.schedules[dateIso] ?: continue
            val baseDate = try {
                LocalDate.parse(dateIso)
            } catch (_: Exception) {
                continue
            }

            for ((startStr, endStr) in day.intervals) {
                val warnKey = "$dateIso $startStr"
                if (warnKey in warned) continue
                val parts = startStr.split(":")
                if (parts.size < 2) continue
                val h = parts[0].toIntOrNull() ?: continue
                val m = parts[1].toIntOrNull() ?: continue
                if (h !in 0..23) continue

                val startZdt = ZonedDateTime.of(baseDate.year, baseDate.monthValue, baseDate.dayOfMonth, h, m, 0, 0, AppConfig.KYIV_ZONE)
                val minsUntil = Duration.between(now, startZdt).toMinutes()

                if (minsUntil in 5..35) {
                    warned.add(warnKey)
                    val title = "⏳ Відключення о $startStr (до $endStr)"
                    val body = "Через ~$minsUntil хв за графіком"
                    NotificationHelper.sendShortAlert(context, title, body)
                    store.addHistoryEvent("⏳", title, body)
                }
            }
        }

        store.saveWarnedKeys(warned)
    }

    private fun scheduleNextPreOutageCheck(
        context: Context,
        state: DtekState,
        todayIso: String,
        tomorrowIso: String
    ) {
        val now = DtekParser.nowKyiv()
        var bestDelayMin: Long? = null

        for (dateIso in listOf(todayIso, tomorrowIso)) {
            val day = state.schedules[dateIso] ?: continue
            val baseDate = try {
                LocalDate.parse(dateIso)
            } catch (_: Exception) {
                continue
            }
            for ((startStr, _) in day.intervals) {
                val parts = startStr.split(":")
                if (parts.size < 2) continue
                val h = parts[0].toIntOrNull() ?: continue
                val m = parts[1].toIntOrNull() ?: continue
                if (h !in 0..23) continue
                val startZdt = ZonedDateTime.of(baseDate.year, baseDate.monthValue, baseDate.dayOfMonth, h, m, 0, 0, AppConfig.KYIV_ZONE)
                val targetAlert = startZdt.minusMinutes(20)
                val delayMin = Duration.between(now, targetAlert).toMinutes()
                if (delayMin in 2..720) {
                    if (bestDelayMin == null || delayMin < bestDelayMin) {
                        bestDelayMin = delayMin
                    }
                }
            }
        }

        if (bestDelayMin != null) {
            val req = OneTimeWorkRequestBuilder<DtekSyncWorker>()
                .setInitialDelay(bestDelayMin, TimeUnit.MINUTES)
                .build()
            WorkManager.getInstance(context).enqueueUniqueWork(
                PRE_WARN_WORK_NAME,
                ExistingWorkPolicy.REPLACE,
                req
            )
        }
    }
}

class DtekSyncWorker(
    appContext: Context,
    params: WorkerParameters
) : Worker(appContext, params) {
    override fun doWork(): Result {
        DtekSyncManager.fetchAndProcess(applicationContext)
        return Result.success()
    }
}
"""

# ------------------------------------------------------------------------------
# 6. Kotlin: D10WidgetProvider.kt (9-Б Напівпрозорий 4x1 Glass)
# ------------------------------------------------------------------------------

WIDGET_PROVIDER_KT = r"""
package ua.dnipro.d10svitlo

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.widget.RemoteViews
import java.time.Instant
import java.time.format.DateTimeFormatter

class D10WidgetProvider : AppWidgetProvider() {

    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray
    ) {
        updateAllWidgets(context)
    }

    override fun onReceive(context: Context, intent: Intent) {
        super.onReceive(context, intent)
        if (intent.action == ACTION_WIDGET_REFRESH) {
            DtekSyncManager.triggerImmediateSync(context)
            updateAllWidgets(context)
        }
    }

    companion object {
        const val ACTION_WIDGET_REFRESH = "ua.dnipro.d10svitlo.WIDGET_REFRESH"

        fun updateAllWidgets(context: Context) {
            val manager = AppWidgetManager.getInstance(context)
            val ids = manager.getAppWidgetIds(ComponentName(context, D10WidgetProvider::class.java))
            if (ids.isEmpty()) return

            val store = AppStore(context)
            val state = store.getCachedState()
            val light = DtekParser.computeTrafficLight(state)

            val barRes = when (light.level) {
                2 -> R.drawable.widget_bar_terracotta
                1 -> R.drawable.widget_bar_ochre
                else -> R.drawable.widget_bar_mint
            }

            val syncMs = store.getLastSyncEpochMs()
            val timeStr = if (syncMs > 0) {
                Instant.ofEpochMilli(syncMs)
                    .atZone(AppConfig.KYIV_ZONE)
                    .format(DateTimeFormatter.ofPattern("HH:mm"))
            } else {
                "--:--"
            }

            val openIntent = Intent(context, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            val openPi = PendingIntent.getActivity(
                context,
                10,
                openIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )

            val refreshIntent = Intent(context, D10WidgetProvider::class.java).apply {
                action = ACTION_WIDGET_REFRESH
            }
            val refreshPi = PendingIntent.getBroadcast(
                context,
                11,
                refreshIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )

            for (id in ids) {
                val rv = RemoteViews(context.packageName, R.layout.widget_d10)
                rv.setImageViewResource(R.id.widget_bar, barRes)
                rv.setTextViewText(R.id.widget_title, light.title)
                rv.setTextViewText(R.id.widget_subtitle, light.subtitle)
                rv.setTextViewText(R.id.widget_time, timeStr)
                rv.setOnClickPendingIntent(R.id.widget_text_box, openPi)
                rv.setOnClickPendingIntent(R.id.widget_refresh_btn, refreshPi)
                manager.updateAppWidget(id, rv)
            }
        }
    }
}
"""

# ------------------------------------------------------------------------------
# 7. Kotlin: MainActivity.kt (Увесь дизайн: 1-Г, 2-Б, 3-Б, 4-В, 5-В, 6-А, 7-Б, 8-Б, 12-Б)
# ------------------------------------------------------------------------------

MAIN_ACTIVITY_KT = r"""
package ua.dnipro.d10svitlo

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.Bundle
import android.text.TextUtils
import android.util.TypedValue
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.Switch
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import java.time.Instant
import java.time.format.DateTimeFormatter
import java.util.concurrent.Executors

/**
 * 3-Б: Один годинний «цеглинковий» сегмент 24-годинної шкали з підтримкою півгодин (first/second).
 */
class HourBrickView(
    context: Context,
    private val leftColor: Int,
    private val rightColor: Int,
    private val hourText: String,
    private val isCurrentHour: Boolean,
    private val nowBorderColor: Int
) : View(context) {

    private val fillPaint = Paint(Paint.ANTI_ALIAS_FLAG)
    private val borderPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeWidth = 2f * resources.displayMetrics.density
        color = nowBorderColor
    }
    private val textPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.WHITE
        textAlign = Paint.Align.CENTER
        typeface = Typeface.DEFAULT_BOLD
        textSize = 9.5f * resources.displayMetrics.scaledDensity
    }
    private val clipPath = Path()
    private val rectF = RectF()
    private val radius = 5f * resources.displayMetrics.density

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val w = width.toFloat()
        val h = height.toFloat()
        if (w <= 0f || h <= 0f) return

        rectF.set(0f, 0f, w, h)
        clipPath.reset()
        clipPath.addRoundRect(rectF, radius, radius, Path.Direction.CW)

        val saveCount = canvas.save()
        canvas.clipPath(clipPath)

        fillPaint.color = leftColor
        canvas.drawRect(0f, 0f, w / 2f + 0.5f, h, fillPaint)

        fillPaint.color = rightColor
        canvas.drawRect(w / 2f, 0f, w, h, fillPaint)

        canvas.restoreToCount(saveCount)

        if (isCurrentHour) {
            val halfStroke = borderPaint.strokeWidth / 2f
            rectF.set(halfStroke, halfStroke, w - halfStroke, h - halfStroke)
            canvas.drawRoundRect(rectF, radius, radius, borderPaint)
        }

        val textY = h / 2f - (textPaint.descent() + textPaint.ascent()) / 2f
        canvas.drawText(hourText, w / 2f, textY, textPaint)
    }
}

class MainActivity : AppCompatActivity() {

    // 4-В: М'яка пастельна палітра (бережна до очей)
    private val colorMint = Color.parseColor("#2A9D8F")
    private val colorTerracotta = Color.parseColor("#C85555")
    private val colorOchre = Color.parseColor("#D4A348")
    private val colorAccentBlue = Color.parseColor("#60A5FA")

    private lateinit var store: AppStore
    private val executor = Executors.newSingleThreadExecutor()

    private var activeTab: Int = 0 // 0 = Світло, 1 = Історія, 2 = Налашт.
    private var selectedDayTab: Int = 0 // 0 = Сьогодні, 1 = Завтра
    private var isSyncing: Boolean = false
    private var isOfflineLastAttempt: Boolean = false

    private lateinit var contentContainer: LinearLayout
    private lateinit var refreshBtn: TextView
    private lateinit var groupChip: TextView
    private lateinit var navButtons: List<LinearLayout>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        store = AppStore(this)
        NotificationHelper.ensureChannels(this)
        DtekSyncManager.schedulePeriodicSync(this)

        buildRootLayout()
        requestNotificationPermissionIfNeeded()
        renderCurrentTab()
        runManualSync(silentToast = true)
    }

    override fun onDestroy() {
        super.onDestroy()
        executor.shutdownNow()
    }

    private fun isDarkTheme(): Boolean {
        val mask = resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK
        return mask == Configuration.UI_MODE_NIGHT_YES
    }

    private fun dp(v: Int): Int = (v * resources.displayMetrics.density).toInt()

    private fun textPrimary(): Int =
        if (isDarkTheme()) Color.parseColor("#F1F5F9") else Color.parseColor("#0F172A")

    private fun textMuted(): Int =
        if (isDarkTheme()) Color.parseColor("#94A3B8") else Color.parseColor("#475569")

    private fun glassBgColor(): Int =
        if (isDarkTheme()) Color.parseColor("#1AFFFFFF") else Color.parseColor("#CCFFFFFF")

    private fun glassBorderColor(): Int =
        if (isDarkTheme()) Color.parseColor("#2EFFFFFF") else Color.parseColor("#221E293B")

    private fun glassPillColor(): Int =
        if (isDarkTheme()) Color.parseColor("#24FFFFFF") else Color.parseColor("#140F172A")

    private fun makeGlassDrawable(radiusDp: Int = 16, fillOverride: Int? = null, borderOverride: Int? = null): GradientDrawable {
        return GradientDrawable().apply {
            cornerRadius = dp(radiusDp).toFloat()
            setColor(fillOverride ?: glassBgColor())
            setStroke(dp(1), borderOverride ?: glassBorderColor())
        }
    }

    private fun requestNotificationPermissionIfNeeded() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU && !NotificationHelper.hasPermission(this)) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                1001
            )
        }
    }

    private fun buildRootLayout() {
        // 1-Г: Виразний атмосферний градієнт фону
        val bgColors = if (isDarkTheme()) {
            intArrayOf(
                Color.parseColor("#0F172A"),
                Color.parseColor("#162447"),
                Color.parseColor("#1B1B2F")
            )
        } else {
            intArrayOf(
                Color.parseColor("#DDE7F5"),
                Color.parseColor("#EEF3FA"),
                Color.parseColor("#E2ECF7")
            )
        }

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            background = GradientDrawable(GradientDrawable.Orientation.TL_BR, bgColors)
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
            )
        }

        // Верхня компактна панель (12-Б: кнопка оновлення + кнопка поділитись)
        val topBar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(dp(14), dp(12), dp(14), dp(8))
        }

        val titleBox = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        }

        val titleTv = TextView(this).apply {
            text = "⚡ Д10 Світло"
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 17f)
            typeface = Typeface.DEFAULT_BOLD
        }

        groupChip = TextView(this).apply {
            setTextColor(textMuted())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 11f)
            typeface = Typeface.DEFAULT_BOLD
            background = makeGlassDrawable(99, fillOverride = glassPillColor())
            setPadding(dp(8), dp(3), dp(8), dp(3))
            val lp = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
            lp.marginStart = dp(8)
            layoutParams = lp
            visibility = View.GONE
        }

        titleBox.addView(titleTv)
        titleBox.addView(groupChip)

        val shareBtn = makeHeaderIconButton("📤") { shareCurrentSchedule() }
        refreshBtn = makeHeaderIconButton("↻") { runManualSync(silentToast = false) }
        (refreshBtn.layoutParams as LinearLayout.LayoutParams).marginStart = dp(8)

        topBar.addView(titleBox)
        topBar.addView(shareBtn)
        topBar.addView(refreshBtn)
        root.addView(topBar)

        // Прокручувана область контенту
        val scroll = ScrollView(this).apply {
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                0,
                1f
            )
            isFillViewport = true
        }

        contentContainer = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(12), dp(4), dp(12), dp(16))
        }
        scroll.addView(contentContainer)
        root.addView(scroll)

        // 6-А: Нижня панель вкладок (3 кнопки)
        val bottomBar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            background = GradientDrawable().apply {
                setColor(if (isDarkTheme()) Color.parseColor("#CC111827") else Color.parseColor("#E6FFFFFF"))
                setStroke(dp(1), glassBorderColor())
            }
            setPadding(dp(6), dp(6), dp(6), dp(8))
        }

        val tabsSpec = listOf(
            Triple(0, "⚡", "Світло"),
            Triple(1, "📜", "Історія"),
            Triple(2, "⚙️", "Налашт.")
        )
        navButtons = tabsSpec.map { (idx, ico, label) ->
            val btn = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                gravity = Gravity.CENTER
                setPadding(dp(4), dp(4), dp(4), dp(4))
                layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
                setOnClickListener {
                    if (activeTab != idx) {
                        activeTab = idx
                        updateNavStyles()
                        renderCurrentTab()
                    }
                }
            }
            val icoTv = TextView(this).apply {
                text = ico
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 15f)
                gravity = Gravity.CENTER
            }
            val lblTv = TextView(this).apply {
                text = label
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 11f)
                gravity = Gravity.CENTER
            }
            btn.addView(icoTv)
            btn.addView(lblTv)
            bottomBar.addView(btn)
            btn
        }

        root.addView(bottomBar)
        setContentView(root)
        updateNavStyles()
    }

    private fun makeHeaderIconButton(symbol: String, onClick: () -> Unit): TextView {
        return TextView(this).apply {
            text = symbol
            gravity = Gravity.CENTER
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 15f)
            typeface = Typeface.DEFAULT_BOLD
            background = makeGlassDrawable(12)
            layoutParams = LinearLayout.LayoutParams(dp(36), dp(36))
            setOnClickListener { onClick() }
        }
    }

    private fun updateNavStyles() {
        navButtons.forEachIndexed { idx, btn ->
            val lbl = btn.getChildAt(1) as TextView
            if (idx == activeTab) {
                lbl.setTextColor(colorMint)
                lbl.typeface = Typeface.DEFAULT_BOLD
            } else {
                lbl.setTextColor(textMuted())
                lbl.typeface = Typeface.DEFAULT
            }
        }
    }

    private fun runManualSync(silentToast: Boolean) {
        if (isSyncing) return
        isSyncing = true
        refreshBtn.text = "…"

        executor.execute {
            val res = DtekSyncManager.fetchAndProcess(applicationContext)
            runOnUiThread {
                isSyncing = false
                refreshBtn.text = "↻"
                isOfflineLastAttempt = !res.ok
                renderCurrentTab()
                if (!silentToast) {
                    val msg = if (res.ok) "Дані оновлено" else "Офлайн — показано кеш"
                    Toast.makeText(this, msg, Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    private fun shareCurrentSchedule() {
        val text = DtekParser.buildShareText(store.getCachedState())
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, text)
        }
        startActivity(Intent.createChooser(intent, "Поділитись графіком"))
    }

    private fun renderCurrentTab() {
        val state = store.getCachedState()
        val groupLabel = state?.let { DtekParser.formatGroupPretty(it.groupId) }.orEmpty()
        if (groupLabel.isNotEmpty()) {
            groupChip.text = groupLabel
            groupChip.visibility = View.VISIBLE
        } else {
            groupChip.visibility = View.GONE
        }

        contentContainer.removeAllViews()
        when (activeTab) {
            0 -> renderHomeTab(state)
            1 -> renderHistoryTab()
            2 -> renderSettingsTab()
        }
    }

    // ==========================================================================
    // ВКЛАДКА 0: ГОЛОВНИЙ КОМПАКТНИЙ ДАШБОРД (2-Б, 3-Б, 5-В, 7-Б, 8-Б)
    // ==========================================================================

    private fun renderHomeTab(state: DtekState?) {
        val light = DtekParser.computeTrafficLight(state)
        val statusColor = when (light.level) {
            2 -> colorTerracotta
            1 -> colorOchre
            else -> colorMint
        }

        // 2-Б: Картка статусу з акцентною полосою зліва (спокійна вночі)
        val heroOuter = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            background = makeGlassDrawable(14)
            setPadding(dp(10), dp(10), dp(12), dp(10))
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { bottomMargin = dp(8) }
        }

        val leftBar = View(this).apply {
            background = GradientDrawable().apply {
                cornerRadius = dp(4).toFloat()
                setColor(statusColor)
            }
            layoutParams = LinearLayout.LayoutParams(dp(5), ViewGroup.LayoutParams.MATCH_PARENT).apply {
                marginEnd = dp(10)
            }
        }

        val heroBody = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        }

        val topRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        topRow.addView(TextView(this).apply {
            text = "● ${light.title}"
            setTextColor(statusColor)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 14f)
            typeface = Typeface.DEFAULT_BOLD
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        })

        val syncMs = store.getLastSyncEpochMs()
        if (syncMs > 0L) {
            val hhmm = Instant.ofEpochMilli(syncMs)
                .atZone(AppConfig.KYIV_ZONE)
                .format(DateTimeFormatter.ofPattern("HH:mm"))
            topRow.addView(TextView(this).apply {
                text = "↻ $hhmm"
                setTextColor(textMuted())
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 10.5f)
            })
        }
        heroBody.addView(topRow)

        heroBody.addView(TextView(this).apply {
            text = light.subtitle
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 12.5f)
            setPadding(0, dp(2), 0, 0)
        })

        heroBody.addView(TextView(this).apply {
            text = AppConfig.ADDRESS_SHORT
            setTextColor(textMuted())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 11f)
            setPadding(0, dp(2), 0, 0)
        })

        // Бейдж застарілих даних (>40 хв) або офлайн-режиму
        val staleMinutes = DtekParser.minutesSinceServerCheck(state)
        if (isOfflineLastAttempt) {
            heroBody.addView(makeStalePill("📡 Офлайн-режим • показано збережений кеш"))
        } else if (staleMinutes != null && staleMinutes > 40) {
            heroBody.addView(makeStalePill("⏱ Дані ДТЕК востаннє перевірялись $staleMinutes хв тому"))
        }

        heroOuter.addView(leftBar)
        heroOuter.addView(heroBody)
        contentContainer.addView(heroOuter)

        // 7-Б: Табличка фактів аварії та перенесень (коли є активна аварія)
        if (state != null && state.banner.active) {
            contentContainer.addView(buildOutageFactTableCard(state))
        }

        // Картка графіка ГПВ (Сьогодні / Завтра + 3-Б цеглинки + 5-В повна стрічка)
        contentContainer.addView(buildScheduleDashboardCard(state))
    }

    private fun makeStalePill(msg: String): TextView {
        return TextView(this).apply {
            text = msg
            setTextColor(colorOchre)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 10.5f)
            typeface = Typeface.DEFAULT_BOLD
            background = makeGlassDrawable(
                8,
                fillOverride = Color.parseColor("#26D4A348"),
                borderOverride = Color.parseColor("#55D4A348")
            )
            setPadding(dp(8), dp(3), dp(8), dp(3))
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { topMargin = dp(6) }
        }
    }

    // 7-Б: Табличка фактів (ключ — значення)
    private fun buildOutageFactTableCard(state: DtekState): LinearLayout {
        val card = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            background = makeGlassDrawable(14)
            setPadding(dp(12), dp(10), dp(12), dp(10))
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { bottomMargin = dp(8) }
        }

        card.addView(TextView(this).apply {
            text = "Деталі відключення (ДТЕК)"
            setTextColor(textMuted())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 11f)
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, dp(6))
        })

        val b = state.banner
        val hist = state.endDateHistory
        val deltaSuffix = if (hist.size >= 2) {
            val prevDt = DtekParser.parseDtekDateTime(hist[hist.size - 2])
            val currDt = DtekParser.parseDtekDateTime(hist.last())
            if (prevDt != null && currDt != null) " (${DtekParser.formatDeltaUa(prevDt, currDt)})" else ""
        } else ""

        addFactRow(card, "Причина", b.reason.ifBlank { "Відсутня електроенергія" }, textPrimary(), true)
        if (b.startDate.isNotEmpty()) {
            addFactRow(card, "Початок", b.startDate, textPrimary(), false)
        }
        if (b.endDate.isNotEmpty()) {
            addFactRow(card, "Відновлення", "до ${b.endDate}$deltaSuffix", colorTerracotta, true)
        }
        if (hist.size >= 2) {
            val shiftsCount = hist.size - 1
            val chain = hist.takeLast(4).joinToString(" → ") { DtekParser.shortEndTime(it) }
            addFactRow(card, "Перенесень", "$shiftsCount ($chain)", colorOchre, false)
        }
        if (b.updateTimestamp.isNotEmpty()) {
            addFactRow(card, "Оновлено ДТЕК", b.updateTimestamp, textMuted(), false)
        }

        return card
    }

    private fun addFactRow(parent: LinearLayout, key: String, value: String, valueColor: Int, bold: Boolean) {
        val row = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(0, dp(3), 0, dp(3))
        }
        row.addView(TextView(this).apply {
            text = key
            setTextColor(textMuted())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 11.5f)
            layoutParams = LinearLayout.LayoutParams(dp(106), ViewGroup.LayoutParams.WRAP_CONTENT)
        })
        row.addView(TextView(this).apply {
            text = value
            setTextColor(valueColor)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 11.5f)
            typeface = if (bold) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
            gravity = Gravity.END
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        })
        parent.addView(row)
    }

    private fun buildScheduleDashboardCard(state: DtekState?): LinearLayout {
        val card = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            background = makeGlassDrawable(14)
            setPadding(dp(11), dp(10), dp(11), dp(10))
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
        }

        val now = DtekParser.nowKyiv()
        val todayIso = now.toLocalDate().toString()
        val tomorrowIso = now.toLocalDate().plusDays(1).toString()
        val todaySched = state?.schedules?.get(todayIso)
        val tomorrowSched = state?.schedules?.get(tomorrowIso)

        // Перемикач вкладок «Сьогодні» / «Завтра»
        val segRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            background = makeGlassDrawable(10, fillOverride = glassPillColor())
            setPadding(dp(3), dp(3), dp(3), dp(3))
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { bottomMargin = dp(8) }
        }

        val todayTitle = "Сьогодні (${todaySched?.dateLabel?.take(5) ?: now.format(DateTimeFormatter.ofPattern("dd.MM"))})"
        val tomorrowTitle = if (tomorrowSched != null) {
            "Завтра (${tomorrowSched.dateLabel.take(5)})"
        } else {
            "Завтра (ще немає)"
        }

        segRow.addView(makeDaySwitchBtn(todayTitle, selectedDayTab == 0) {
            selectedDayTab = 0
            renderCurrentTab()
        })
        segRow.addView(makeDaySwitchBtn(tomorrowTitle, selectedDayTab == 1) {
            selectedDayTab = 1
            renderCurrentTab()
        })
        card.addView(segRow)

        val currentDay = if (selectedDayTab == 0) todaySched else tomorrowSched
        if (currentDay == null) {
            card.addView(TextView(this).apply {
                text = if (selectedDayTab == 1) {
                    "ДТЕК ще не опублікував графік на завтра.\nЩойно він з'явиться — прийде сповіщення."
                } else {
                    "Графік ГПВ на сьогодні відсутній у даних ДТЕК."
                }
                setTextColor(textMuted())
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 12f)
                gravity = Gravity.CENTER
                setPadding(dp(8), dp(22), dp(8), dp(22))
            })
            return card
        }

        val slots = DtekParser.buildHalfHourSlots(currentDay)
        val offMins = slots.count { it == 1 } * 30
        val maybeMins = slots.count { it == 2 } * 30
        val onMins = 1440 - offMins - maybeMins

        // Компактний підсумок дня (8-Б)
        val statsRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, 0, 0, dp(6))
        }
        val summaryParts = mutableListOf(
            "🟢 ${DtekParser.formatDurationUa(onMins)}",
            "🪫 ${DtekParser.formatDurationUa(offMins)}"
        )
        if (maybeMins > 0) summaryParts.add("🟡 ${DtekParser.formatDurationUa(maybeMins)}")

        statsRow.addView(TextView(this).apply {
            text = summaryParts.joinToString("  •  ")
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 11.5f)
            typeface = Typeface.DEFAULT_BOLD
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        })
        if (selectedDayTab == 0) {
            statsRow.addView(TextView(this).apply {
                text = "рамка = зараз"
                setTextColor(textMuted())
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 10f)
            })
        }
        card.addView(statsRow)

        // 3-Б: 24-годинна шкала цеглинками (2 ряди по 12 годин)
        val currentHour = now.hour
        val isToday = selectedDayTab == 0
        card.addView(buildBrickRow(slots, 0, 11, isToday, currentHour))
        card.addView(buildBrickRow(slots, 12, 23, isToday, currentHour))

        // Розділювач
        card.addView(View(this).apply {
            setBackgroundColor(glassBorderColor())
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                dp(1)
            ).apply {
                topMargin = dp(8)
                bottomMargin = dp(6)
            }
        })

        // 5-В: Повна стрічка дня (і вікна зі світлом, і без світла)
        val segments = DtekParser.buildTimelineSegments(currentDay)
        val nowMin = now.hour * 60 + now.minute

        for (seg in segments) {
            val isNowSeg = isToday && nowMin in seg.startMin until seg.endMin
            val isPastSeg = isToday && seg.endMin <= nowMin

            val (dot, segColor, labelWord) = when (seg.status) {
                1 -> Triple("🪫", colorTerracotta, "без світла")
                2 -> Triple("🟡", colorOchre, "можливе")
                else -> Triple("🟢", colorMint, "зі світлом")
            }

            val row = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                setPadding(dp(8), dp(5), dp(8), dp(5))
                alpha = if (isPastSeg) 0.52f else 1f
                if (isNowSeg) {
                    background = makeGlassDrawable(
                        9,
                        fillOverride = Color.argb(38, Color.red(segColor), Color.green(segColor), Color.blue(segColor)),
                        borderOverride = segColor
                    )
                }
                layoutParams = LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.WRAP_CONTENT
                ).apply { bottomMargin = dp(3) }
            }

            val rangeText = "${DtekParser.minutesToHHMM(seg.startMin)} — ${DtekParser.minutesToHHMM(seg.endMin)}"
            row.addView(TextView(this).apply {
                text = "$dot $rangeText"
                setTextColor(if (seg.status == 0) textPrimary() else segColor)
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 12f)
                typeface = if (seg.status != 0 || isNowSeg) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
                layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
            })

            val durText = "${DtekParser.formatDurationUa(seg.endMin - seg.startMin)} $labelWord"
            row.addView(TextView(this).apply {
                text = if (isNowSeg) "ЗАРАЗ • $durText" else durText
                setTextColor(if (isNowSeg) segColor else textMuted())
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 11f)
                typeface = if (isNowSeg) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
            })

            card.addView(row)
        }

        return card
    }

    private fun makeDaySwitchBtn(label: String, active: Boolean, onClick: () -> Unit): TextView {
        return TextView(this).apply {
            text = label
            gravity = Gravity.CENTER
            maxLines = 1
            ellipsize = TextUtils.TruncateAt.END
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 11.5f)
            typeface = if (active) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
            setTextColor(if (active) Color.WHITE else textMuted())
            background = if (active) {
                GradientDrawable().apply {
                    cornerRadius = dp(8).toFloat()
                    setColor(colorMint)
                }
            } else {
                null
            }
            setPadding(dp(6), dp(6), dp(6), dp(6))
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
            setOnClickListener { onClick() }
        }
    }

    private fun buildBrickRow(
        slots: IntArray,
        fromHour: Int,
        toHour: Int,
        isToday: Boolean,
        currentHour: Int
    ): LinearLayout {
        val row = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { bottomMargin = dp(4) }
        }
        val nowOutline = if (isDarkTheme()) Color.WHITE else Color.parseColor("#0F172A")

        for (h in fromHour..toHour) {
            val cLeft = slotColor(slots[h * 2])
            val cRight = slotColor(slots[h * 2 + 1])
            val brick = HourBrickView(
                context = this,
                leftColor = cLeft,
                rightColor = cRight,
                hourText = h.toString(),
                isCurrentHour = isToday && h == currentHour,
                nowBorderColor = nowOutline
            ).apply {
                layoutParams = LinearLayout.LayoutParams(0, dp(23), 1f).apply {
                    marginStart = dp(1)
                    marginEnd = dp(1)
                }
            }
            row.addView(brick)
        }
        return row
    }

    private fun slotColor(status: Int): Int = when (status) {
        1 -> colorTerracotta
        2 -> colorOchre
        else -> colorMint
    }

    // ==========================================================================
    // ВКЛАДКА 1: ІСТОРІЯ ПОДІЙ (ОСТАННІ 20)
    // ==========================================================================

    private fun renderHistoryTab() {
        val history = store.getHistory()

        val headerRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(dp(2), dp(2), dp(2), dp(8))
        }
        headerRow.addView(TextView(this).apply {
            text = "Історія подій (${history.size}/${AppConfig.MAX_HISTORY_ITEMS})"
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 14f)
            typeface = Typeface.DEFAULT_BOLD
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        })
        if (history.isNotEmpty()) {
            headerRow.addView(TextView(this).apply {
                text = "Очистити"
                setTextColor(colorTerracotta)
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 12f)
                typeface = Typeface.DEFAULT_BOLD
                setPadding(dp(8), dp(4), dp(4), dp(4))
                setOnClickListener {
                    store.clearHistory()
                    renderCurrentTab()
                }
            })
        }
        contentContainer.addView(headerRow)

        if (history.isEmpty()) {
            val emptyCard = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                background = makeGlassDrawable(14)
                setPadding(dp(16), dp(24), dp(16), dp(24))
                gravity = Gravity.CENTER
            }
            emptyCard.addView(TextView(this).apply {
                text = "Журнал поки порожній.\nТут з'являтимуться всі аварії, переноси та зміни графіків."
                setTextColor(textMuted())
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 12.5f)
                gravity = Gravity.CENTER
            })
            contentContainer.addView(emptyCard)
            return
        }

        for (ev in history) {
            val card = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                background = makeGlassDrawable(12)
                setPadding(dp(11), dp(8), dp(11), dp(8))
                layoutParams = LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.WRAP_CONTENT
                ).apply { bottomMargin = dp(6) }
            }

            val top = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
            }
            top.addView(TextView(this).apply {
                text = ev.title
                setTextColor(textPrimary())
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 12.5f)
                typeface = Typeface.DEFAULT_BOLD
                layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
            })
            top.addView(TextView(this).apply {
                text = ev.timeLabel
                setTextColor(textMuted())
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 10.5f)
            })
            card.addView(top)

            if (ev.subtitle.isNotBlank()) {
                card.addView(TextView(this).apply {
                    text = ev.subtitle
                    setTextColor(textMuted())
                    setTextSize(TypedValue.COMPLEX_UNIT_SP, 11.5f)
                    setPadding(0, dp(2), 0, 0)
                })
            }
            contentContainer.addView(card)
        }
    }

    // ==========================================================================
    // ВКЛАДКА 2: НАЛАШТУВАННЯ (ТИХІ ГОДИНИ 6-Г, ТЕСТ СПОВІЩЕННЯ)
    // ==========================================================================

    private fun renderSettingsTab() {
        var s = store.getSettings()

        val card = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            background = makeGlassDrawable(14)
            setPadding(dp(14), dp(12), dp(14), dp(12))
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { bottomMargin = dp(10) }
        }

        card.addView(TextView(this).apply {
            text = "Сповіщення та тихі години"
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 14f)
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, dp(8))
        })

        card.addView(makeSwitchRow("Сповіщення увімкнено", s.notificationsEnabled) { checked ->
            s = s.copy(notificationsEnabled = checked)
            store.saveSettings(s)
        })

        card.addView(makeSwitchRow("Тихі години вночі", s.quietEnabled) { checked ->
            s = s.copy(quietEnabled = checked)
            store.saveSettings(s)
            renderCurrentTab()
        })

        if (s.quietEnabled) {
            card.addView(makeHourStepperRow("Початок тихих годин", s.quietStartHour) { newHour ->
                s = s.copy(quietStartHour = newHour)
                store.saveSettings(s)
                renderCurrentTab()
            })
            card.addView(makeHourStepperRow("Кінець тихих годин", s.quietEndHour) { newHour ->
                s = s.copy(quietEndHour = newHour)
                store.saveSettings(s)
                renderCurrentTab()
            })
            card.addView(
                makeSwitchRow("Вночі без звуку (інакше вимкнути)", s.quietSilentOnly) { checked ->
                    s = s.copy(quietSilentOnly = checked)
                    store.saveSettings(s)
                }
            )
        }

        val testBtn = Button(this).apply {
            text = "🔔 Тестове сповіщення"
            isAllCaps = false
            setTextColor(Color.WHITE)
            background = GradientDrawable().apply {
                cornerRadius = dp(10).toFloat()
                setColor(colorMint)
            }
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { topMargin = dp(10) }
            setOnClickListener {
                if (!NotificationHelper.hasPermission(this@MainActivity)) {
                    requestNotificationPermissionIfNeeded()
                    Toast.makeText(this@MainActivity, "Дозвольте сповіщення для Д10 Світло", Toast.LENGTH_SHORT).show()
                } else {
                    NotificationHelper.sendShortAlert(
                        this@MainActivity,
                        "⚡ Д10 Світло працює!",
                        "Фонова перевірка активна (кожні 30 хв)",
                        isTest = true
                    )
                    Toast.makeText(this@MainActivity, "Тестове сповіщення надіслано", Toast.LENGTH_SHORT).show()
                }
            }
        }
        card.addView(testBtn)
        contentContainer.addView(card)

        // Картка джерела даних
        val srcCard = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            background = makeGlassDrawable(14)
            setPadding(dp(14), dp(12), dp(14), dp(12))
        }
        srcCard.addView(TextView(this).apply {
            text = "Джерело даних (GitHub state.json)"
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 13f)
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, dp(6))
        })

        val urlInput = EditText(this).apply {
            setText(s.stateUrl)
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 11.5f)
            background = makeGlassDrawable(8, fillOverride = glassPillColor())
            setPadding(dp(10), dp(8), dp(10), dp(8))
            maxLines = 2
        }
        srcCard.addView(urlInput)

        val saveUrlBtn = Button(this).apply {
            text = "Зберегти URL та перевірити"
            isAllCaps = false
            setTextColor(Color.WHITE)
            background = GradientDrawable().apply {
                cornerRadius = dp(10).toFloat()
                setColor(colorAccentBlue)
            }
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { topMargin = dp(8) }
            setOnClickListener {
                val u = urlInput.text.toString().trim()
                s = s.copy(stateUrl = u.ifEmpty { AppConfig.DEFAULT_STATE_URL })
                store.saveSettings(s)
                Toast.makeText(this@MainActivity, "URL збережено", Toast.LENGTH_SHORT).show()
                runManualSync(silentToast = false)
            }
        }
        srcCard.addView(saveUrlBtn)

        srcCard.addView(TextView(this).apply {
            text = "Фонова перевірка: кожні 30 хв • Версія 1.0.0\nАдреса: ${AppConfig.ADDRESS_SHORT}"
            setTextColor(textMuted())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 11f)
            setPadding(0, dp(10), 0, 0)
        })

        contentContainer.addView(srcCard)
    }

    private fun makeSwitchRow(label: String, checked: Boolean, onChanged: (Boolean) -> Unit): LinearLayout {
        val row = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, dp(6), 0, dp(6))
        }
        row.addView(TextView(this).apply {
            text = label
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 12.5f)
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        })
        row.addView(Switch(this).apply {
            isChecked = checked
            setOnCheckedChangeListener { _, isChecked -> onChanged(isChecked) }
        })
        return row
    }

    private fun makeHourStepperRow(label: String, hour: Int, onChange: (Int) -> Unit): LinearLayout {
        val row = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, dp(5), 0, dp(5))
        }
        row.addView(TextView(this).apply {
            text = label
            setTextColor(textMuted())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 12f)
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        })

        val minus = TextView(this).apply {
            text = "−"
            gravity = Gravity.CENTER
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 16f)
            typeface = Typeface.DEFAULT_BOLD
            background = makeGlassDrawable(8, fillOverride = glassPillColor())
            layoutParams = LinearLayout.LayoutParams(dp(32), dp(30))
            setOnClickListener { onChange((hour + 23) % 24) }
        }
        val valTv = TextView(this).apply {
            text = String.format("%02d:00", hour)
            gravity = Gravity.CENTER
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 12.5f)
            typeface = Typeface.DEFAULT_BOLD
            layoutParams = LinearLayout.LayoutParams(dp(54), ViewGroup.LayoutParams.WRAP_CONTENT)
        }
        val plus = TextView(this).apply {
            text = "+"
            gravity = Gravity.CENTER
            setTextColor(textPrimary())
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 16f)
            typeface = Typeface.DEFAULT_BOLD
            background = makeGlassDrawable(8, fillOverride = glassPillColor())
            layoutParams = LinearLayout.LayoutParams(dp(32), dp(30))
            setOnClickListener { onChange((hour + 1) % 24) }
        }
        row.addView(minus)
        row.addView(valTv)
        row.addView(plus)
        return row
    }
}
"""


def main() -> None:
    write_file("settings.gradle.kts", SETTINGS_GRADLE)
    write_file("build.gradle.kts", ROOT_BUILD_GRADLE)
    write_file("gradle.properties", GRADLE_PROPERTIES)
    write_file("app/build.gradle.kts", APP_BUILD_GRADLE)

    write_file("app/src/main/AndroidManifest.xml", ANDROID_MANIFEST)
    write_file("app/src/main/res/values/themes.xml", THEMES_XML)
    write_file("app/src/main/res/values-night/themes.xml", THEMES_NIGHT_XML)

    write_file("app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml", IC_LAUNCHER_XML)
    write_file("app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml", IC_LAUNCHER_XML)
    write_file("app/src/main/res/drawable/ic_launcher_background.xml", IC_LAUNCHER_BG)
    write_file("app/src/main/res/drawable/ic_launcher_foreground.xml", IC_LAUNCHER_FG)
    write_file("app/src/main/res/drawable/ic_notif_bolt.xml", IC_NOTIF_BOLT)

    write_file("app/src/main/res/xml/d10_widget_info.xml", WIDGET_INFO_XML)
    write_file("app/src/main/res/drawable/widget_glass_bg.xml", WIDGET_GLASS_BG)
    write_file("app/src/main/res/drawable/widget_bar_mint.xml", WIDGET_BAR_MINT)
    write_file("app/src/main/res/drawable/widget_bar_ochre.xml", WIDGET_BAR_OCHRE)
    write_file("app/src/main/res/drawable/widget_bar_terracotta.xml", WIDGET_BAR_TERRACOTTA)
    write_file("app/src/main/res/layout/widget_d10.xml", WIDGET_LAYOUT_XML)

    pkg = "app/src/main/java/ua/dnipro/d10svitlo"
    write_file(f"{pkg}/ModelsAndStore.kt", MODELS_AND_STORE_KT)
    write_file(f"{pkg}/NotificationHelper.kt", NOTIFICATION_HELPER_KT)
    write_file(f"{pkg}/DtekSyncManager.kt", SYNC_MANAGER_KT)
    write_file(f"{pkg}/D10WidgetProvider.kt", WIDGET_PROVIDER_KT)
    write_file(f"{pkg}/MainActivity.kt", MAIN_ACTIVITY_KT)

    print("Android project generated successfully in ./android_build")


if __name__ == "__main__":
    main()
  
