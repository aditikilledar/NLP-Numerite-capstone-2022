import React from "react";
import commonStyles from "../styles/Common.module.css";
import styles from "../styles/WordProblems.module.css";
import flask from '../public/flask1.svg';
import Image from "next/image";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFlask } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";

export default function WordProblems(props){
    const [problem, setProblem] = React.useState('');
    const [solution, setSolution] = React.useState('solution will appear here');
    const [loading, setLoading] = React.useState(false);
    function handleProblemChange(e) {
        setProblem(e.target.value);
    }
    function handleClick(e){
        //setSolve(!solve);
        setLoading(true);
        setSolution('');
        // fetch solution from server and display it
        let data = {"mwp": problem}
        axios.post('http://localhost:5000/api/mwp', data).then(res => {
            setSolution(res.data);
            setLoading(false);
        }).catch(err => {
            setSolution('something went wrong :(');
            setLoading(false);
        })
        console.log('solved')
    }
    return(
        <div className={commonStyles.centeredDiv}>
            <div className={commonStyles.pageHead}>
                <p className={commonStyles.title}>Word Problem Solver</p>
            </div>
            <div className={styles.container}>
                <div className={styles.questionContainer}>
                    <p>Enter word problem here</p>
                    <textarea placeholder="> " value={problem} className={styles.wpInput} onChange={handleProblemChange}>
                    </textarea>
                    <a className={styles.submit} onClick={handleClick}>
                        <FontAwesomeIcon icon={faFlask} /> solve
                    </a>
                </div>
                <div className={styles.solution}>
                    <img src='/flask.svg' className={loading ? styles.bgImage : styles.bgImageHidden}/>
                    <p>{solution.solution}</p>
                </div>
            </div>
        </div>    
    )
}