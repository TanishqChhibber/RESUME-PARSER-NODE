const express = require('express');
const { parseResume } = require('../controllers/resumeParser');

const router = express.Router();

router.post('/parse', parseResume);

module.exports = router;
