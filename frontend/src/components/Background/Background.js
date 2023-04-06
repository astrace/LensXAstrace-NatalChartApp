import React from 'react';
import Image from 'next/image';
import styles from './Background.module.css'
import background from '../../../public/background-image.png';

export default function Background() {
  return (
    <div className={styles.bgWrap}>
      <Image
        alt="background"
        src={background}
        placeholder="blur"
        quality={100}
        fill
        sizes="100vw"
        style={{
          objectFit: 'cover',
        }}
      />
    </div>
  )
}
