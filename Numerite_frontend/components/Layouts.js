import React from "react";
import styles from '../styles/Layouts.module.css'
import HomeButton from "./HomeButton";
import Image from "next/image";

const Layout = ({ children }) => {
  return (
  <>
  <main className={styles.main}>
    {children}
    <HomeButton />
  </main>
  <div className={styles.footer}>
    <p>PW_AMJ_04</p>
  {/* <p>&copy; {new Date().getFullYear()}</p> */}
  {/* <Image src="/pes.png" alt="Next.js" height={50} width={50} /> */}
  </div>
  </>
  );
}

export default Layout;