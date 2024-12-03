# 코난조

이 프로젝트는 **블록깨기 게임**을 **Pygame**을 사용해서 만들었습니다.

## 목차
- [멤버](#멤버)
- [다운로드](#exe-다운로드-for-windows)
- [인게임 화면](#인게임-화면)
- [소개](#소개)
- [ChatGPT가 생성한 최초 버전](#최초-버전)
- [조작법](#조작법)

-----
## 멤버

- 장진석 20241499
- 정현국 20241502
- 고지호 20241505
- 최은성 20242531
- 김건우 20241493
- 김수한 20200915
- 양경윤 20222589

-------

# exe 다운로드 (For Windows)  

## [다운로드 (최신 릴리즈)](https://github.com/Jinseok2419342/Conan/releases/latest)
## [바로 실행 가능](https://github.com/Jinseok2419342/Conan/releases/latest)

-----

# 인게임 화면

## **1. 시작 화면** 
- 시작 화면에서는 "Press Space To Start" 메시지가 표시됩니다.
- 플레이어는 스페이스바를 눌러 게임을 시작할 수 있습니다.
<img src="https://github.com/user-attachments/assets/e79e679b-6f49-4b87-9fe1-a6ea10679e9b" width="50%" height="50%">


## **2. 플레이 화면**
- 벽돌, 패들, 공이 화면에 표시되며 게임이 진행됩니다.
- 화면 상단에는 점수, 경과 시간, 게임 횟수가 표시됩니다.
<img src="https://github.com/user-attachments/assets/976beabb-dbdd-4bdc-a1dd-cde2c373c75e" width="50%" height="50%">
<br><br>

- 스테이지가 지날 수록 여러번 충돌해야 깨지는 `강화 벽돌`들이 점점 더 많아집니다.  
- (해당 `강화 벽돌`들은 테두리에만 연하게 회색 보호막이 있습니다)
<img src="https://github.com/user-attachments/assets/bb3014e3-ed65-43f3-8420-d00563c290b5" width="50%" height="50%">

<br><br>
- 노란색 네모는 패들 크기 증가
- 노란색 원은 공 갯수 추가
- 회색 네모는 랜덤 위치에 절대 깨지지 않는 블록 추가
<img src="https://github.com/user-attachments/assets/916c8876-80a8-4393-a7c4-5c58cedafeb8" width="50%" height="50%">



## **3. 게임 오버**
- 공이 모두 바닥에 떨어지면 "Game Over" 화면이 표시됩니다.
- 플레이어는 스페이스바를 눌러 게임을 재시작할 수 있습니다.
<img src="https://github.com/user-attachments/assets/d70bc3dd-c64d-496e-ac26-55b65b5869aa" width="50%" height="50%">


## **4. 게임 클리어**

### 스테이지 클리어
- 모든 벽돌을 제거하면 "Game Clear" 화면이 표시됩니다.
- 스페이스바를 눌러 다음 스테이지를 진행할 수 있습니다.
<img src="https://github.com/user-attachments/assets/7cdbd8d0-9124-4fc0-81c1-b724de8cc93e" width="50%" height="50%">

<br>

### 게임 클리어
- 10스테이지를 클리어 시.
- 게임이 완전히 클리어 됩니다.
<img src="https://github.com/user-attachments/assets/fbeb0d38-2463-46fb-8dba-3deb8509fdf6" width="50%" height="50%">



## **5. 일시정지**
- 게임 도중 ESC 혹은 SPACE 키를 누르면 게임이 일시정지 됩니다.
- 일시정지 동안 타이머는 흐르지 않으며 다시 ESC 또는 SPACE 키를 눌러서 다시 이어서 할 수 있습니다.
<img src="https://github.com/user-attachments/assets/8c093c7b-2b11-409d-8090-4a2323382f1c" width="50%" height="50%">



-----

# 소개

## 벽돌깨기 게임(Breakout Game)의 게임 개요

`벽돌깨기`는 플레이어가 패들을 조작하여 공을 튕겨서 벽돌들을 제거하는 아케이드 게임입니다.   
게임에는 다양한 색상의 벽돌, 특별한 아이템들, 파괴 불가능한 벽돌, 여러번 충돌해야 파괴되는 벽돌과 여러 스테이지 등이 포함되어 있으며,

각 스테이지의 모든 벽돌을 제거하여 10스테이지까지 모든 스테이지를 클리어하는 것이 목표인 게임 입니다.

----


### **1. 기본 메커니즘**
- **패들 조작**:
  - 화살표 키(`←`, `→`) 또는 `A`, `D` 키를 사용해 패들을 좌우로 이동합니다.
- **공 이동**:
  - 공은 벽, 패들, 벽돌 등과 충돌하면 튕깁니다.
- **벽돌 제거**:
  - 공이 벽돌과 충돌하면 벽돌이 제거되고, 점수가 증가합니다.
- **패들 판정**
  - 패들의 어느 부분에 공이 튀기냐에 따라 공의 속도가 달라집니다.
  - 추가로 패들이 늘어난 상태에서 끝쪽에 공이 맞으면 공이 훨씬 더 빨라집니다

### **2. 아이템**
- **패들 크기 증가 아이템**:
  - 패들의 좌우 길이가 증가합니다.
- **공 개수 증가 아이템**:
  - 추가 공이 생성되어 여러 공을 동시에 다룰 수 있습니다.
- **파괴 불가능한 벽돌 생성 아이템**:
  - 제거할 수 없는 회색 벽돌이 새로 생성됩니다.

### **3. 스테이지**
- 모든 벽돌을 부수면 다음 스테이지로 이동하게 됩니다.
- 총 10스테이지까지 있습니다.
- 스테이지가 진행될 수록 여러번 타격해야 사라지는 `강화 벽돌` 수가 많아집니다.
- 스테이지가 진행될 수록 공의 최대 속도가 더 빨라집니다.
- f키를 누르면 10스테이지로 이동 가능(이전 스테이지들은 스킵 됨)

### **4. 점수 및 시간**
- **점수 계산**:
  - 벽돌 제거 시 10점이 추가됩니다.
- **경과 시간**:
  - 게임 시작부터의 경과 시간이 상단에 표시됩니다.
  - 일시정지 동안은 타이머 시간이 흐르지 않습니다.
- **게임 횟수**:
  - 현재 진행 중인 게임 횟수가 표시됩니다.
  - 클리어 후 다시 게임 시작시 게임 횟수가 초기화 됩니다.


---

## 최초 버전
ChatGPT가 생성한 최초 버전입니다. ( gif 이미지 )  

![gpt_first](https://github.com/user-attachments/assets/06657891-16fa-496b-845b-564d36715004)

-----

## 조작법
| 키보드 입력 | 동작                              |
|-------------|-----------------------------------|
| `←`, `A`    | 패들을 왼쪽으로 이동              |
| `→`, `D`    | 패들을 오른쪽으로 이동            |
| `SPACE`     | 게임 시작 / 일시정지 / 재시작      |
| `ESC`       | 일시정지 / 재시작              |

-----

