package PruebasActions;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import org.junit.jupiter.api.*;

import org.junit.jupiter.api.*;
import org.openqa.selenium.*;

import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;
import io.github.bonigarcia.wdm.WebDriverManager;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class RobustTest {

    private static ExtentReports extent;
    private ExtentTest test;
    private WebDriver driver;

    @BeforeAll
    public static void setupReport() {
        // Inicializa el reportero Spark
        ExtentSparkReporter spark = new ExtentSparkReporter("target/ExtentReport.html");
        extent = new ExtentReports();
        extent.attachReporter(spark);
    }

    @BeforeEach
    public void setup(TestInfo testInfo) {
        // Crea una entrada para cada prueba individual
        test = extent.createTest(testInfo.getDisplayName());

        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless", "--no-sandbox", "--disable-dev-shm-usage");
        driver = new ChromeDriver(options);
        
        test.info("Navegador inicializado");
    }

    @Test
    public void testRobustFlujoCompleto() {
        test.info("Iniciando flujo de login...");
        // ... tu lógica de prueba ...
        test.pass("Login exitoso y producto agregado al carrito");
    }

    @AfterEach
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @AfterAll
    public static void tearDownReport() {
        // Obligatorio para generar el archivo final
        extent.flush();
    }
}