import React, { useRef } from "react";
import styles from "../styles/Card.module.css";
import Image from "next/image";

const Card = (props) => {
  const link = useRef(null);
  return (
      <div className={styles.card} onClick={() => link.current.click()}>
        <div className={styles.cardHeader}>
          <Image src={`/${props.src}`} alt="Next.js" height={150} width={150} className={styles.Image}/>
          <p className={styles.cardTitle}>{props.title}</p>
        </div>
        <div className={styles.cardBody}>
          <p>{props.body}</p>
          <a ref={link} href={props.linkTo} className={styles.cardButton}>Get started with {props.title} </a>
        </div>
      </div>    
    )
}

export default Card;