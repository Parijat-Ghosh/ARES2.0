const { spawn } = require('child_process');
const path = require('path');

exports.analyzeDisasterImage = (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: "No image uploaded" });
    }

    const imagePath = req.file.path;
    const pythonScriptPath = path.join(__dirname, '../module3_vision/vision_pipeline.py');

    const pythonProcess = spawn('python', [pythonScriptPath, '--image', imagePath]);

    let outputData = '';
    let errorData = '';

    pythonProcess.stdout.on('data', (data) => {
        outputData += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        errorData += data.toString();
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`Python script exited with code ${code}`);
            console.error(`Error details: ${errorData}`);
            return res.status(500).json({ error: "Failed to process image through vision pipeline" });
        }

        try {
            const analysisResult = JSON.parse(outputData);
            return res.status(200).json(analysisResult);
        }

        catch (parseError) {
            console.error("Failed to parse Python output:", outputData);
            return res.status(500).json({ error: "Invalid response format from vision pipeline" });
        }
    });
};
