import Head from 'next/head'
import Image from 'next/image'
import commonStyles from '../styles/Common.module.css'
import styles from '../styles/Home.module.css'

import Card from '../components/Card'
import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [hello, setHello] = useState('');
  useEffect(() => {
    axios.get('http://localhost:5000/').then(res => {
      console.log(res);
      setHello(res.data);
      console.log(hello);
    })
  })
  return (
    <div className={styles.home}>
      <h1 className={commonStyles.title}>Numerite</h1>
      <div className={styles.container}>
        <Card src="undraw_writing.svg" title="Essays" linkTo='/essay' />
        <Card src="undraw_maths.svg" title="Word Problems" linkTo='/word-problems'/>
      </div>
      <div className={styles.centeredDiv}>
        <p>
          {/*
            content here
          */}
        </p>
      </div>
    </div>
  )
}
