import React, { useEffect, useRef, useState } from "react";
import styles from "../styles/Essay.module.css";
import commonStyles from "../styles/Common.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";

export default function Essay(props){
    const [prompts, setPrompts] = useState([]);
    const [prompt, setPrompt] = useState("");
    const [essay, setEssay] = useState('');

    useEffect(() => {
        // fetch prompts from the database
        setPrompts([
            'prompt1', 'prompt2', 'prompt3', 'prompt4', 'prompt5', 'prompt6', 'prompt7', 'prompt8', 'prompt9', 'prompt10'
        ])
    }, [])

    const handleSubmit = (e) => {
        e.preventDefault();
        const data = {
            prompt: prompt,
            essay: essay
        }
        console.log(data);
        // axios.post('/api/essay', data)
        //     .then(res => {
        //         console.log(res)
        //     }).catch(err => {
        //         console.log(err)
        //     })
    }
    function wordCount(str) {
        return str.split(/\s+/).length - 1;
    }

    return(
        <div className={commonStyles.centeredDiv}>
            <div className={commonStyles.pageHead}>
                <p className={commonStyles.title}>Essay Assessment</p>
            </div>
            <div className={styles.essayInput}>
                <div className={styles.prompt}>
                    <p>Prompt</p>
                    <select className={styles.select} onChange={(e) => setPrompt(e.target.value)} value={prompt}>
                        {
                            prompts.map((prompt, index) => {
                                return <option key={index}>{prompt}</option>
                            })
                        }
                    </select>
                    <button href='/essay' className={styles.submitEssay} onClick={handleSubmit}>
                        <FontAwesomeIcon icon={faPaperPlane} />
                    </button>
                </div>
                <div className={styles.essayContainer}>
                    <textarea value={essay} onChange={(e) => setEssay(e.target.value)} className={styles.textarea} placeholder="Write your essay here..."></textarea>
                    <p className={styles.wordCount}>{wordCount(essay)} words</p>
                </div>
            </div>
        </div>
    )
}