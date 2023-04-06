import React from 'react';
import Image from "next/image";
import styles from './Icon.module.css'

export default function Icon(props) {
  return (
    <Image src={props.src} alt="icon" width={props.width} height={props.height} />
  )
}

