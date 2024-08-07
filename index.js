
const {app, BrowserWindow} = require("electron")
const { spawn, exec } = require("child_process");


let serverProcess;  // Variable para almacenar el proceso del servidor
let npmProcess;     // Variable para almacenar el proceso de npm


function getServerProcess() {
    return new Promise((resolve, reject) => {
        exec('tasklist', (err, stdout) => {
            if (err) {
                return reject(err);
            }
            // Verificar si el proceso de Django está en ejecución
            const isRunning = stdout.toLowerCase().includes("manage.py");
            resolve(isRunning);
        });
    });
}

async function startServer() {
    const isRunning = await getServerProcess();
    if (!isRunning) {
        // Si no está en ejecución, iniciar el proceso
        serverProcess = spawn('python', ['manage.py', 'runserver'], { shell: true });

        serverProcess.stdout.on('data', (data) => {
            console.log(`Servidor: ${data}`);
        });

        serverProcess.stderr.on('data', (data) => {
            console.error(`Error del servidor: ${data}`);
        });
    } else {
        console.log("El servidor ya está en ejecución.");
    }
}


function ElectronMainMethod(){



    const launchWindow = new BrowserWindow({
        title: "Facturas",
        width: 777,
        height: 444,
        webPreferences: {
            nodeIntegration: true, // Enable Node.js integration if needed
            contextIsolation: false // Disable context isolation if needed
        }
    });

    const appURL = "http://127.0.0.1:8000";

    launchWindow.loadURL(appURL).catch((error) => {
        console.error('Error loading URL:', error);
    });

    launchWindow.on('closed', () => {
        if (serverProcess) {
            serverProcess.kill();  // Detener el proceso del servidor si fue iniciado aquí
        }
        app.quit(); // Cerrar la aplicación
    });


}//fin del main


// Iniciar la aplicación
app.whenReady().then(async () => { 
    await startServer();
    ElectronMainMethod();  // Llamar a la función principal
});
