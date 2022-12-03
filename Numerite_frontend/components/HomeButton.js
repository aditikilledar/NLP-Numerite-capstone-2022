import React from "react";
import styles from "../styles/HomeButton.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHome } from "@fortawesome/free-solid-svg-icons";
import Link from "next/link";

const HomeButton = () => {
    return (
        <Link href="/" className={styles.link}>
            <div className={styles.circleDiv}>
            <FontAwesomeIcon icon={faHome} />
            </div>
        </Link>
    )
}

export default HomeButton;