import React, { useState } from 'react';
import axios from 'axios';
import {
    Container,
    Typography,
    TextField,
    Button,
    Paper,
    List,
    ListItem,
    ListItemText,
    LinearProgress,
    Accordion,
    AccordionSummary,
    AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

function App() {
    const [resumeFile, setResumeFile] = useState(null);
    const [jdFile, setJdFile] = useState(null);
    const [matchData, setMatchData] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleResumeChange = (event) => setResumeFile(event.target.files[0]);
    const handleJdChange = (event) => setJdFile(event.target.files[0]);

    const handleSubmit = async () => {
        setLoading(true);
        setMatchData(null);
        const formData = new FormData();
        formData.append('resume', resumeFile);
        formData.append('jd', jdFile);

        try {
            const response = await axios.post('http://127.0.0.1:5000/match', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            setMatchData(response.data);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container maxWidth="md" style={{ marginTop: '50px' }}>
            <Typography variant="h4" align="center" gutterBottom>
                Resume Matcher
            </Typography>
            <TextField
                type="file"
                fullWidth
                margin="normal"
                onChange={handleResumeChange}
                label="Upload Resume (.txt or .pdf)"
                InputLabelProps={{ shrink: true }}
            />
            <TextField
                type="file"
                fullWidth
                margin="normal"
                onChange={handleJdChange}
                label="Upload Job Description (.txt or .pdf)"
                InputLabelProps={{ shrink: true }}
            />
            <Button
                variant="contained"
                color="primary"
                onClick={handleSubmit}
                disabled={loading}
                style={{ marginTop: '20px' }}
            >
                Match
            </Button>
            {loading && <LinearProgress style={{ marginTop: '10px' }} />}

            {matchData && (
                <Paper elevation={3} style={{ marginTop: '30px', padding: '20px' }}>
                    <Typography variant="h6" gutterBottom>
                        Match Score: {matchData.match_score.toFixed(2)}
                    </Typography>
                    <Typography variant="h6" gutterBottom>
                        Suggestions:
                    </Typography>
                    {Object.keys(matchData.suggestions).map((category) => (
                        <Accordion key={category}>
                            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                <Typography variant="subtitle1">{category}</Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                                <List>
                                    {matchData.suggestions[category].map((suggestion, index) => (
                                        <ListItem key={index}>
                                            <ListItemText primary={suggestion} />
                                        </ListItem>
                                    ))}
                                </List>
                            </AccordionDetails>
                        </Accordion>
                    ))}
                </Paper>
            )}
        </Container>
    );
}

export default App;