import random as rd
import time
import math
import operator

startNum = 100

# 2차원 배열 하나에 개체의 인덱스와 각 개체의 형질을 부여한다. 형질은 5개.
gene = [[0 for col in range(7)] for row in range(startNum)]  # 100마리로 시작
# 0 : 먹이의 종류, 1 : 털의 유무 /여기까진 0 또는 1의 값
# 2 : 말단부의 크기(0~5 정수), 3 : 필요 수분(0~5 실수), 4 : 몸집 크기(1~5 실수), 5 : 에너지, 6: 성별 (수컷 : 0, 암컷 : 1)
environment = list(0 for i in range(2))

mutantRate = int(input('돌연변이가 발생할 확률(역수로 적용됨) : '))  # 돌연변이가 일어날 확률 1/mutantRate
generation = 1  # 현재 몇 세대인지 카운트
food = 500  # 각 개체가 매 세대마다 1씩 먹고, 그 후에 수가 foodReproduceRate 만큼 증가함(몇%씩)
foodReproduceRate = 1.3
e1 = 100
e2 = -100


# ------------------ 변수 선언 끝 ------------------ #


def state():
    cnt1, cnt2, cnt3 = 0, 0, 0  # cnt1 : 인덱스가 1인, 즉 육식동물의 수. cnt2 : 털이 있는 동물의 수. cnt3 : 수컷 수
    tail = 0
    water = 0
    size = 0  # 위의 세 변수들은 현재 개체의 값들의 합 (후에 개체수로 나누어 평균을 구하는 용도)
    for i in range(len(gene)):
        if gene[i][0] == 1:
            cnt1 += 1
        if gene[i][1] == 1:
            cnt2 += 1
        if gene[i][6] == 0:
            cnt3 += 1
        tail += gene[i][2]
        water += gene[i][3]
        size += gene[i][4]
    print('--------------------------------')
    print('현재 개체 수 : ' + str(len(gene)))
    print('수컷 개체 수 : ' + str(cnt3))
    print('암컷 개체 수 : ' + str(len(gene) - cnt3))
    print('육식동물의 수 : ' + str(cnt1))
    print('초식동물의 수 : ' + str(len(gene) - cnt1))
    print('털이 달린 동물의 수(%) : ' + str(round(((cnt2/len(gene)) * 100), 2)))
    print('말단부 크기의 평균 : ' + str(round((tail / len(gene)), 2)))
    print('필요한 수분의 평균 : ' + str(round((water/len(gene)), 2)))
    print('몸집의 크기의 평균 : ' + str(round((size / len(gene)), 2)))
    print()
    print('현재 환경 \n온도 : ' + str(environment[0]) + '\n습도 : ' + str(environment[1]))
    print('--------------------------------')


def eat_plant(a):  # a는 초식동물인 모든 유전자
    global food
    x = sort(a)  # 에너지가 높은 인덱스 순서로 정렬된 리스트
    for i in range(len(x)):
        gene[x[i]][5] += 1  # 먹은 애들은 에너지 +1
    food -= 2 * len(x)  # 초식동물 수 * 2만큼 감소


def eat_animal(a):  # a는 육식동물
    # 에너지 + 몸집 이 1.5배 이상이면 먹을 수 있음
    sort(a)
    for i in range(len(a)):
        flag = False
        for t in range(len(a) - 1):
            if ((gene[i][4] + gene[i][5]) >= 1.5 * (gene[t][4] + gene[t][5])) and gene[t][5] > 0:
                gene[i][5] += 2  # 먹어서 에너지 +2
                gene[t][5] = -1  # 죽음
                flag = True
                break


def eat():  # 현재 모든 유전자를 입력받아 초식, 육식동물로 구분
    plant = list()
    animal = list()  # 먹이의 종류
    for i in range(len(gene)):
        if gene[i][0] == 0:  # 초식동물
            plant.append(i)
        else:
            animal.append(i)  # 육식동물
    eat_plant(plant)
    eat_animal(animal)


def sort(a):  # a는 특정 조건을 만족하는 개체들의 인덱스 리스트
    energy_of_a = list()  # a의 인덱스 번호 순서대로 개체들의 에너지가 입력
    for i in a:
        energy_of_a.append(gene[i][5])

    index_and_energy = dict()
    for i in range(len(a)):
        index_and_energy[a[i]] = energy_of_a[i]
    result = sorted(index_and_energy.items(), key=operator.itemgetter(1), reverse=True)  # 튜플이 원소인 리스트

    b = list()
    for i in range(len(a)):
        b.append(result[i][0])

    return b  # 에너지가 높은 인덱스 순으로 정렬된 리스트 리턴


def energy():  # 자세한 숫자는 변동이 필요함
    # 세대가 지날 때 마다(energy()가 호출) 모든 개체의 에너지를 일정량 만큼 깎는다.
    for i in range(len(gene)):
        gene[i][5] -= 2

    # 환경[0](온도)에 영향 : foodReproduceRate, 1, 2, 4  (온도 : 0 ~ 30)
    # 환경[1](습도)에 영향 : foodReproduceRate, 3  (습도 : 0 ~ 100)
    global foodReproduceRate
    if environment[0] < 10:  # 온도 낮음
        foodReproduceRate = 1.1  # 풀의 재생산력 낮아짐
        for i in range(len(gene)):
            if gene[i][1] == 1:
                gene[i][5] += 1  # 깎이고 1추가 되므로 결국은 깎이긴 하나, 털이 있는 친구들이 이점이 있음
            gene[i][5] += 2 - gene[i][2]  # 온도가 낮으므로 말단부가 작은 친구들이 이점이 있음
            gene[i][5] += gene[i][4] - 3  # 온도가 낮으므로 몸집이 큰 친구들이 이점이 있음

    elif 10 <= environment[0] < 20:  # 온도 중간
        foodReproduceRate = 1.3
        # 극단적인 친구들만 손해가 가고, 나머지는 그대로

        if gene[i][2] == 0.1 or gene[i][2] == 5:
            gene[i][5] -= 2
        if gene[i][4] == 0 or gene[i][4] == 5:
            gene[i][5] -= 2

    elif 20 <= environment[0] <= 30:  # 온도 높음
        foodReproduceRate = 1.5  # 풀의 재생산력 높아짐
        for i in range(len(gene)):
            if gene[i][1] == 0:
                gene[i][5] += 2  # 깎이고 추가 되므로 결국 깎이긴 하나, 털이 없는 친구들이 이점이 있음
            gene[i][5] += gene[i][2] - 3  # 온도가 높으므로 말단부가 큰 친구들이 이점이 있음
            gene[i][5] += 2 - gene[i][4]  # 온도가 높으므로 몸집이 작은 친구들이 이점이 있음

    # 습도에 따른 에너지 영향
    if environment[1] < 50:  # 습도 낮음
        for i in range(len(gene)):
            gene[i][5] += 2 - gene[i][3]  # 습도가 낮으면 필요 수분이 적을 수록 유리

    # 어떤 경우에도 에너지가 안깎이는 개체가 있어선 안됨
    # ** 테스트 **  최소 에너지 출력


def remove_all_occur(a, i):
    try:
        while True:
            a.remove(i)
    except ValueError:
        pass


def death():
    # gene[i][5]가 0이하인 객체는 배열에서 제거
    rm_index = list()  # 제거할 객체들의 인덱스
    for i in range(len(gene)):
        if gene[i][5] <= 0:
            rm_index.append(i)  # 제거할 객체들 목록 작성
    for i in rm_index:
        gene[i] = 0  # 바로 삭제해버리면 인덱스 오류나므로 0으로 표시한 후 삭제는 따로
    remove_all_occur(gene, 0)


def birth():
    healthy_male = list()
    healthy_female = list()

    # 1. 번식 가능한 개체 리스트 작성 (암 수 따로)
    for i in range(len(gene)):
        if gene[i][5] >= 3:
            if gene[i][6] == 0:  # 수컷이면
                healthy_male.append(i)
            else:
                healthy_female.append(i)

    # 2. 에너지 높은 순으로 정렬
    healthy_male = sort(healthy_male)
    healthy_female = sort(healthy_female)

    # 3. 0번끼리, 1번끼리 번식하는 것으로 생각, 성별이 더 많은 쪽은 번식 못하는 개체 발생 (일부일처제로 가정)
    # 4. 각 형질을 생성할 때 마다 돌연변이 체크, 이상 없을 시 (0, 0)이면 0, (1, 1)이면 1, 그 외에는 랜덤으로
    # 5. 돌연변이 발생 시 (0, 0)이면 1, (1, 1)이면 0, 그 외에는 랜덤으로
    # 6. 0 또는 1이 아닌 경우 값의 평균을, 돌연변이 발생시 최댓값 혹은 최솟값 중 하나로
    # 7. 인덱스 0, 1은 0아니면 1의 값, 그 외에는 평균
    for i in range(min(len(healthy_male), len(healthy_female))):
        gene[healthy_male[i]][5] -= 2
        gene[healthy_female[i]][5] -= 2

        child = list()
        for k in range(2):  # 0또는 1의 값을 갖는 경우 (육식/초식, 털O/X)
            is_mutant = rd.randrange(mutantRate)  # 0 ~ mutantRate 까지 정수 0이 되면 돌연변이로 생각
            if is_mutant == 0:  # 돌연변이 발생
                if gene[healthy_male[i]][k] == gene[healthy_female[i]][k] == 0:
                    child.append(1)
                elif gene[healthy_male[i]][k] == gene[healthy_female[i]][k] == 1:
                    child.append(0)
                else:
                    child.append(rd.randrange(2))
            else:  # 정상적인 상황
                if gene[healthy_male[i]][k] == gene[healthy_female[i]][k]:
                    child.append(gene[healthy_female[i]][k])
                else:
                    child.append(rd.randrange(2))
        for k in range(2, 5):  # k = 2, 3, 4
            is_mutant = rd.randrange(mutantRate)
            if is_mutant == 0:
                r = rd.randrange(2)  # 0이면 수컷 정보, 1이면 암컷 정보
                if r == 0:
                    child.append(gene[healthy_male[i]][k])
                else:
                    child.append(gene[healthy_female[i]][k])
            else:
                child.append((gene[healthy_male[i]][k] + gene[healthy_female[i]][k]) / 2)

        child.append(10)  # 에너지
        child.append(rd.randrange(2))  # 성별

        gene.append(child)  # 리스트 맨 끝에 추가
        del child

# ------------------ 함수 선언 끝 ------------------ #

# 1. 랜덤으로 각 개체의 형질을 부여해야 함


for i in range(startNum):
    for j in range(2):
        gene[i][j] = rd.randrange(0, 2)
    gene[i][2] = rd.randrange(0, 6)  # 말단부 크기
    gene[i][3] = rd.uniform(0.1, 5)  # 필요 수분
    gene[i][4] = rd.uniform(1, 5)  # 몸집의 크기
    gene[i][5] = 10  # 남은 에너지는 10으로 초기화
    gene[i][6] = rd.randrange(0, 2)  # 성별은 0(수컷) 또는 1(암컷)

# 2. 사용자가 환경에 대한 정보 부여
environment[0] = int(input('온도를 입력해주세요 (0 ~ 30): '))  # 온도
environment[1] = int(input('습도를 입력해주세요 (1 ~ 100): '))  # 습도

# 3. 시작, 명령어 입력
print('시작 유전자의 수 :' + str(startNum))
print('현재 세대 : 1')
print('입력할 수 있는 명령어\nn : 다음세대로 진행\ns : 현재 상태 보기\na : 자동으로 반복\nq : 결과 보고 종료')

while True:
    com = input('명령어를 입력 : ')
    if com == 'n':
        generation += 1
        print('현재 세대 :' + str(generation))
        # 식사 -> 환경에 따라 각 개체들의 에너지 계산 -> 죽음 판단, 자리 비우기 -> 번식
        eat()
        energy()
        death()
        birth()
        food *= foodReproduceRate

    elif com == 'a':  # 자동으로 2만이 넘을 때까지 반복, 변화 보여줌
        state()
        while len(gene) <= 20000:
            generation += 1
            # 환경에 따라 각 개체들의 에너지 계산 -> 죽음 판단, 자리 비우기 -> 번식
            eat()
            energy()
            death()
            birth()
            food *= foodReproduceRate
        print('현재 세대 :', generation)
        state()
        break

    elif com == 's':
        state()

    elif com == 'q':
        state()
        break

    elif com == 'p':
        for i in range(len(gene)):
            print(gene[i])

    else:
        print('잘못된 명령어 입니다. 다시 입력해주세요.')
        continue

    if len(gene) > 20000:
        print('* 개체수가 20000을 넘었습니다.')
        state()
        break
    if len(gene) <= 0:
        print('모든 개체가 죽었습니다.')
        break

print('프로그램 종료.. 5초후 자동 종료됩니다.')
time.sleep(5)
