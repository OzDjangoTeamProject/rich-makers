## ERD

본 프로젝트는 사용자(User), 계좌(Account), 거래(Transaction) 정보를 관리하기 위한 구조로 설계되었습니다.

- User : 서비스 이용자 정보 관리
- Account : 사용자의 은행 계좌 정보 (1:N)
- Transaction : 계좌별 입출금 거래 내역 (1:N)

![ERD](docs/erd.png)