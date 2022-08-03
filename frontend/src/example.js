import './App.css';
import TextField from '@mui/material/TextField';
import Button from "@mui/material/Button";
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { useState } from 'react';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { Card, Typography } from '@mui/material';
import axios from 'axios';

function App() {
  const [value, setValue] = useState(0);
  const [textInput, setTextInput] = useState("sadsad;adjsad");

  const setDate = (newValue) => {
    setValue(newValue)
  }

  const submitForm = (e) => {
    console.log(value, textInput);
    axios.post("/barabasha", {"query": "test"}).then((resp) => {console.log(resp.data)})
  }

  return (
    <Card style={{textAlign: "center", padding: "10%", width: "50%"}}>
      <Typography variant='h5' style={{marginBottom: "2%"}}>
        Hello world!  
      </Typography>
      <div>
        <TextField style={{marginRight: "1%"}} label="TEST" value={textInput} onChange={(e) => setTextInput(e.target.value)}/>
        {/* {
          textInput === "test" ?
          <p>HI!</p> : <p>NP~</p>
        }
        {textInput} */}
        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <DatePicker
            value={value}
            onChange={setDate}
            renderInput={(params) => <TextField {...params} />}
          />
        </LocalizationProvider>
      </div>
      <div style={{textAlign: "center", margin: "1%"}}>
        <Button variant="outlined" onClick={submitForm}>Submit</Button>
      </div>
    </Card>
  );
}

export default App;
