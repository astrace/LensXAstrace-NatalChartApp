import React from 'react'
import Image from 'next/image';
import styles from '@/styles/Home.module.css'

function Header() {
  return (
    <header className={styles.header}>
      <div className={styles["header-logo"]}>
        <Image
          src="/astrace_text.svg"
          width={200}
          height={30}
        />
      </div>
    </header>
  )
}

export default Header
