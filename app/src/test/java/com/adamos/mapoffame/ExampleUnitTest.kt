package com.adamos.mapoffame

import org.junit.Test
import org.junit.Assert.*
import kotlin.math.abs

/**
 * Example local unit test, which will execute on the development machine (host).
 *
 * See [testing documentation](http://d.android.com/tools/testing).
 */
class ExampleUnitTest {
    @Test
    fun addition_isCorrect() {
        assertEquals(4, 2 + 2)
    }

    private fun formatYear(year: Int, bceLabel: String, ceLabel: String): String {
        return "${abs(year)} ${if (year < 0) bceLabel else ceLabel}"
    }

    @Test
    fun testBceCeFormatting() {
        // Arabic verification for known cases (Ovid, Seneca)
        assertEquals("43 ق.م", formatYear(-43, "ق.م", "م"))
        assertEquals("17 م", formatYear(17, "ق.م", "م"))
        assertEquals("4 ق.م", formatYear(-4, "ق.م", "م"))
        assertEquals("65 م", formatYear(65, "ق.م", "م"))

        // English verification
        assertEquals("1 BC", formatYear(-1, "BC", "AD"))
        assertEquals("1 AD", formatYear(1, "BC", "AD"))
        assertEquals("4 BC", formatYear(-4, "BC", "AD"))
        assertEquals("43 BC", formatYear(-43, "BC", "AD"))
        assertEquals("70 BC", formatYear(-70, "BC", "AD"))
        assertEquals("106 BC", formatYear(-106, "BC", "AD"))
        assertEquals("247 BC", formatYear(-247, "BC", "AD"))
        assertEquals("356 BC", formatYear(-356, "BC", "AD"))
        assertEquals("384 BC", formatYear(-384, "BC", "AD"))
        assertEquals("470 BC", formatYear(-470, "BC", "AD"))
        assertEquals("590 BC", formatYear(-590, "BC", "AD"))
        assertEquals("14 AD", formatYear(14, "BC", "AD"))
        assertEquals("19 AD", formatYear(19, "BC", "AD"))
        assertEquals("43 AD", formatYear(43, "BC", "AD"))
        assertEquals("65 AD", formatYear(65, "BC", "AD"))

        // Boundary test: 1 BC must not equal 1 AD
        assertNotEquals(formatYear(-1, "BC", "AD"), formatYear(1, "BC", "AD"))
    }
}
