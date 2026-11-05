const express = require('express');
const router = express.Router();
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
const visionController = require('../controllers/visionController');

router.post('/analyze', upload.single('disasterImage'), visionController.analyzeDisasterImage);

module.exports = router;
