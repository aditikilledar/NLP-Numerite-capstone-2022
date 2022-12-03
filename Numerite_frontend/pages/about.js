import React from "react";
import Head from "next/head";
import commonStyles from '../styles/Common.module.css'


export default function About () {
  return (
    <div>
      <h1 className={commonStyles.title}>About</h1>
    </div>
  );
}