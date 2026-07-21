from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, List, Optional, Annotated
from enum import Enum

from datetime import datetime

# 부모 모델 설정
# 객체, 관게 등이 아래의 모델을 상속받아 공통 규제가 적용될 것이다.
class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_to_lower=True,
        str_strip_whitespace=True,
    )

# 객체 목록 정의
class EntityType(str, Enum):
    Company = "Company"
    Person = "Person"
    Government = "Government"
    Industry = "Industry"
    Consumer = "Consumer"
    Event = "Event"
    
    # hyperentity: 많은 객체에 연결 될 수 있고 이를 여러 객체의 속성으로 넣을 수 있는?
    Money = "Money"

    # subentity
    Product = "Product"
    Policy = "Policy"

# 객체의 속성 타입 정의
class CountryType(str, Enum):
    KOREA = "KOREA"
    USA = "USA"



# 모든 객체와 연결 될 메타 속성: 돈, 환율, 지수
class Money(BaseModel):
    time : datetime
    FXRate : int


# 객체 정의
class Company(StrictModel):
    pass

class Government(StrictModel):
    name : CountryType
    power : float = Field(description="국가의 힘")
    gdp : int = Field(description="dollar")

class Person(StrictModel):
    name : str = Field(description="인물의 이름")


## 소비자의 경우 전체적인 관점에서 속성을 정의한다.
class Consumer(StrictModel):
    country : CountryType
    spending_power : int = Field(ge=0, le=1, description="소비자의 소비력")


# 여러 객체를 하나로 묶는 객체의 필요 -> 속성으로 대체? 소비자들의 소비력, 경제 상황, 국가 등




















# ai

class Company(BaseModel):
    id: int | str = Field(description="그 회사의 종목 코드를 그대로 사용한다.")
    name: str = Field(description="회사의 이름")
    coreference: List[str] = Field(description="상호참조를 해결하기 위한 별명 리스트")


class Ontology(BaseModel):
    pass

ONTOLOGY: dict[str, Any] = {
    "entity_types": {
        "NewsArticle": "뉴스 기사",
        "Organization": "기업, 기관, 단체",
        "Person": "사람",
        "Place": "장소 또는 지역",
        "Product": "제품 또는 서비스",
    },
    "relations": {
        "MENTIONS": {
            "domain": ["NewsArticle"],
            "range": ["Organization", "Person", "Place", "Product"],
        },
        "ANNOUNCED": {
            "domain": ["Organization"],
            "range": ["Product"],
            "keywords": ["발표", "공개", "소개"],
        },
        "PARTNERED_WITH": {
            "domain": ["Organization"],
            "range": ["Organization"],
            "keywords": ["협력", "제휴", "파트너십"],
            "symmetric": True,
        },
        "LOCATED_IN": {
            "domain": ["Organization"],
            "range": ["Place"],
            "keywords": ["본사", "위치", "소재"],
        },
        "ANALYZED_BY": {
            "domain": ["Organization"],
            "range": ["Person"],
            "keywords": ["분석가", "언급", "전망"],
        },
    },
}

ATTRIBUTE_SCHEMA: dict[str, dict[str, str]] = {
    "NewsArticle": {
        "mentioned_date": "date",
    },
    "Organization": {
        "market_cap_trillion_krw": "number",
        "revenue_target_trillion_krw": "number",
        "stock_change_percent": "number",
    },
    "Product": {
        "product_category": "string",
    },
    "Person": {
        "role": "string",
    },
    "Place": {
        "admin_area": "string",
    },
}

# 기준선 샘플에서는 기업/제품/사람 객체가 최소한 이 속성을 갖는지 확인한다.
REQUIRED_ATTRIBUTES_BY_TYPE: dict[str, set[str]] = {
    "Organization": {"market_cap_trillion_krw"},
    "Product": {"product_category"},
    "Person": {"role"},
}

ALIAS_KB: dict[str, dict[str, Any]] = {
    "org:samsung-electronics": {
        "name": "삼성전자",
        "entity_type": "Organization",
        "aliases": ["삼성전자", "삼성"],
    },
    "org:sk-hynix": {
        "name": "SK하이닉스",
        "entity_type": "Organization",
        "aliases": ["SK하이닉스", "에스케이하이닉스"],
    },
    "place:seoul": {
        "name": "서울",
        "entity_type": "Place",
        "aliases": ["서울", "서울시", "서초구"],
    },
    "product:exynos-ai": {
        "name": "Exynos AI",
        "entity_type": "Product",
        "aliases": ["Exynos AI", "엑시노스 AI", "차세대 AI 반도체"],
    },
    "person:kim-minsu": {
        "name": "김민수",
        "entity_type": "Person",
        "aliases": ["시장 분석가 김민수", "김민수"],
    },
}

ENTITY_CONFIDENCE_EXACT_ALIAS = 0.95
RELATION_CONFIDENCE_RULE = 0.85
ATTRIBUTE_CONFIDENCE_REGEX = 0.90

print("entity types:", list(ONTOLOGY["entity_types"].keys()))
print("relation types:", list(ONTOLOGY["relations"].keys()))
print("attribute schema:", ATTRIBUTE_SCHEMA)
