# -*- coding: utf-8 -*-
# @project: duspider
# @Author：dyz
# @date：2023/11/8 11:29
# https://go.drugbank.com/drugs/DB00091
import re
import time
from typing import List

from math import ceil
from parsel import Selector
from pydantic import BaseModel

from duspider.base import HEADERS, Spider
from duspider.exceptions import LocationTypeError


class DrugInteraction(BaseModel):
    """药物相互作用"""
    id: str  # DrugBank id
    name: str  # 药物名
    desc: str  # 相互作用
    type: str  # 类型


class DrugBankHit(BaseModel):
    id: str = ''  # DrugBank id
    name: str = ''  # 药物名
    generic_name: str = ''  # 通用名
    synonymes: List = []  # 同义词
    brand_name: str = ''  # 商品名
    background: List = []  # 背景信息
    type: str = ''  # 药物类型
    groups: str = ''  # 类别
    drug_categories: List = []  # 药物类别
    biologic_classification: List = []  # 生物分类
    structure: str = ''  # 结构
    chemical_formula: str = ''  # 化学式
    sequences: str = ''  # 序列
    summary: List = []  # 概述
    indication: List = []  # 适应症
    associated_therapies: str = ''  # 相关疗法
    pharmacodynamics: List = []  # 药效动力学
    mechanism_action: List = []  # 作用机制
    pathways: str = ''  # 作用通路
    pharmacogenomic_effects: str = ''  # 药物基因组学效应
    absorption: List = []  # 吸收
    volume_distribution: List = []  # 分布容积
    protein_binding: List = []  # 蛋白结合
    metabolism: List = []  # 代谢
    half_life: List = []  # 半衰期
    clearance: List = []  # 清除率
    drug_interaction: List[DrugInteraction] = []  # 相互作用
    food_interaction: List = []  # 食物相互作用
    toxicity: List = []  # 毒性

    async def get_drug_interaction(self) -> List[DrugInteraction]:
        """获取药物相互作用"""
        interaction_data = [DrugInteraction()]
        setattr(self, 'drug_interaction', interaction_data)


class DrugBank(Spider):

    def __init__(self, max_retry=3, **kwargs):
        super().__init__()
        self.base_url = 'https://go.drugbank.com/drugs/'
        self.data = {
            "APPROVED": "approved",
            "VET APPROVED": "vet_approved",
            "NUTRACEUTICAL": "nutraceutical",
            "ILLICIT": "illicit",
            "WITHDRAWN": "withdrawn",
            "INVESTIGATIONAL": "investigational",
            "EXPERIMENTAL": "experimental",
            # "ALL DRUGS": "approved",

        }

        self.cookies = {
            'cf_clearance': 'iVXRxn7oiGYaKCn9xvS2Vvh18onAE14BP3qBXxOAdIw-1699411572-0-1-49c08f63.a63988a7.1ec1d083-250.0.0',
            '_ga': 'GA1.1.414772354.1699411591',
            '_clck': '1iz72qk|2|fgj|0|1407',
            '_gcl_au': '1.1.1616239398.1699411594',
            'hubspotutk': '41c7d7c1e3ab76361ec9f970d6f71fe5',
            '__hssrc': '1',
            '__hstc': '49600953.41c7d7c1e3ab76361ec9f970d6f71fe5.1699411596013.1699428178142.1699435168990.4',
            '_omx_drug_bank_session': 'VJRsvDDYUOI9yCgaJl6KFEKKhD%2FPrQupM%2BR1IQfb%2FdHZrOUYg6LwdpaMWtedF9WCuvjZEsEWUOoQccrUoOJlnMdqIv3zCWsxhdV%2FrS72Yg7X8WPJphIKSmg%2BM6frrx29%2F%2Fe98VLjwAZ7HmVuqWJrUxaTYRBmFS1G7p3rqllDrFmqeO7WZQdcXv0x%2BavjLDpf5lKpzu8WkbY73LBJ1%2FoFMMPPYVAQZJnozYGubDBzt2tmoBFrD1BAzZpVIegf5vl2wvWLKSfal2y8n7nwjEOEQsOU9c2nWQsX6JK2eFvBC%2FCrRUlRHt3%2BTun0RBBgY4R9jN%2Fjo%2BSnQ%2FUsk2O6TNhfaRKZKkNr4%2FIwvN8q%2Ftuxl8THsnl%2B03o%3D--%2FhCjuwnK7HfGranh--YZCJ6lHNcfTtZ082h2QBNA%3D%3D',
            '_ga_DDLJ7EEV9M': 'GS1.1.1699443244.6.1.1699443245.59.0.0',
            '_clsk': 'vgvnve|1699443246906|1|1|u.clarity.ms/collect',
        }
        self.headers = {
            'authority': 'go.drugbank.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            # 'cookie': 'cf_clearance=iVXRxn7oiGYaKCn9xvS2Vvh18onAE14BP3qBXxOAdIw-1699411572-0-1-49c08f63.a63988a7.1ec1d083-250.0.0; _ga=GA1.1.414772354.1699411591; _clck=1iz72qk|2|fgj|0|1407; _gcl_au=1.1.1616239398.1699411594; hubspotutk=41c7d7c1e3ab76361ec9f970d6f71fe5; __hssrc=1; __hstc=49600953.41c7d7c1e3ab76361ec9f970d6f71fe5.1699411596013.1699428178142.1699435168990.4; _omx_drug_bank_session=VJRsvDDYUOI9yCgaJl6KFEKKhD%2FPrQupM%2BR1IQfb%2FdHZrOUYg6LwdpaMWtedF9WCuvjZEsEWUOoQccrUoOJlnMdqIv3zCWsxhdV%2FrS72Yg7X8WPJphIKSmg%2BM6frrx29%2F%2Fe98VLjwAZ7HmVuqWJrUxaTYRBmFS1G7p3rqllDrFmqeO7WZQdcXv0x%2BavjLDpf5lKpzu8WkbY73LBJ1%2FoFMMPPYVAQZJnozYGubDBzt2tmoBFrD1BAzZpVIegf5vl2wvWLKSfal2y8n7nwjEOEQsOU9c2nWQsX6JK2eFvBC%2FCrRUlRHt3%2BTun0RBBgY4R9jN%2Fjo%2BSnQ%2FUsk2O6TNhfaRKZKkNr4%2FIwvN8q%2Ftuxl8THsnl%2B03o%3D--%2FhCjuwnK7HfGranh--YZCJ6lHNcfTtZ082h2QBNA%3D%3D; _ga_DDLJ7EEV9M=GS1.1.1699443244.6.1.1699443245.59.0.0; _clsk=vgvnve|1699443246906|1|1|u.clarity.ms/collect',
            'dnt': '1',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        }

    def get_time(self):
        millis = int(round(time.time() * 1000))
        return str(millis)

    def get_params(self, g_type, size=100):
        return {
            'group': g_type,
            'draw': '1',
            'columns[0][data]': '0',
            'columns[0][name]': '',
            'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'true',
            'columns[0][search][value]': '',
            'columns[0][search][regex]': 'false',
            'columns[1][data]': '1',
            'columns[1][name]': '',
            'columns[1][searchable]': 'true',
            'columns[1][orderable]': 'true',
            'columns[1][search][value]': '',
            'columns[1][search][regex]': 'false',
            'start': '0',
            'length': f'{size}',  # 最大
            'search[value]': '',
            'search[regex]': 'false',
            '_': self.get_time(),
        }

    def parse_drug_interactions(self, k, data):
        _list = []
        for row in data:
            _list.append(DrugInteraction(
                id=re.findall("/drugs/(.*?)\">", row[0])[0],
                name=re.findall(">(.*?)</a>", row[0])[0],
                desc=row[1],
                type=k
            ))
        return _list

    async def sem_drug_interactions(self, k, url, params):
        res = await self.get(url, params=params, headers=self.headers, cookies=self.cookies)
        if res:
            print(url, params)
            print(res)
            print(res.text)
            data = res.json()
            info = self.parse_drug_interactions(k, data.get('data', []))
            return info
        return None

    async def get_drug_interactions(self, drug_id):
        url = f'https://go.drugbank.com/drugs/{drug_id}/drug_interactions.json'
        res_list = []
        for k, v in self.data.items():
            params = self.get_params(v)
            res = await self.get(url, params=params, headers=self.headers, cookies=self.cookies)
            if res:
                data = res.json()
                total = data['recordsTotal']
                info = self.parse_drug_interactions(k, data.get('data', []))
                if info:
                    res_list += info
                    pages = ceil(total / 100)
                    for page_ in range(1, pages):
                        params['start'] = f'{page_}'
                        info = self.parse_drug_interactions(k, data.get('data', []))
                        res_list += info
        return res_list

    async def get_drug_interactions2(self, drug_id):
        url = f'https://go.drugbank.com/drugs/{drug_id}/drug_interactions.json'
        task_list = []
        res_list = []
        for k, v in self.data.items():
            params = self.get_params(v)
            res = await self.get(url, params=params, headers=self.headers, cookies=self.cookies)
            if res:
                data = res.json()
                total = data['recordsTotal']
                info = self.parse_drug_interactions(k, data.get('data', []))
                if info:
                    res_list.append(info)
                    pages = ceil(total / 100)
                    for page_ in range(1, pages):
                        task = asyncio.create_task(self.sem_drug_interactions(k, url, params))
                        task_list.append(task)
        if task_list:
            res_data = await asyncio.gather(*task_list)
            res_list += res_data
        return [i for i in res_list if i]

    async def get_data(self, drug_id) -> DrugBankHit:
        """传入id 获取 数据信息"""
        _url = self.base_url + drug_id
        resp = await self.get(_url, headers=self.headers, cookies=self.cookies)
        if resp.history:
            location = resp.history[-1].headers.get('Location')
            location_list = location.split('/')
            if location_list[-2] != 'drugs':
                raise LocationTypeError(_url, msg='跳转后不是drugs', location=location)
            drug_id = location_list[-1]

        data = await self.parse_html(drug_id, resp.text)
        # data.indication = await self.get_drug_interactions(drug_id)  # 获取相互作用

        return data

    def parse_list(self, span_doc):
        """解析列表数据"""
        return [_.xpath('string(.)').get('').strip() for _ in span_doc if _.xpath('string(.)').get('').strip()]

    def parse_mechanism_action(self, doc):
        """解析 mechanism_action"""
        mechanism_action_table = doc.css('#drug-moa-target-table')
        table_t = mechanism_action_table.css('thead > tr > th')
        table_tr = mechanism_action_table.css('tbody > tr')
        ti_list = [i.xpath('string(.)').get('').strip() for i in table_t]
        item_list = []
        for tr in table_tr:
            item = {}
            item[ti_list[0]] = tr.xpath('./td[1]//a/text()').get('').strip()
            item[ti_list[1]] = tr.xpath('./td[2]//div/text()').get('').strip()
            item[ti_list[2]] = tr.xpath('./td[3]/text()').get('').strip()
            if item:
                item_list.append(item)
        return item_list

    async def parse_html(self, drug_id, html) -> DrugBankHit:
        """基于 HTMl 解析数据"""

        doc = Selector(html)

        name = doc.css('div.drug-card h1::text').get('').strip()
        summary_list = doc.xpath('//dt[@id="summary"]/following-sibling::dd[1]/p')
        summary = parse_list(summary_list)

        generic_name = doc.xpath('//dt[@id="generic-name"]/following-sibling::dd[1]/text()').get('').strip()
        brand_name = doc.xpath('string(//dt[@id="brand-names"]/following-sibling::dd[1])').get('').strip()

        background_list = doc.xpath('//dt[@id="background"]/following-sibling::dd[1]/p')
        background = self.parse_list(background_list)
        type = doc.xpath('string(//dt[@id="type"]/following-sibling::dd[1])').get('').strip()


        groups = doc.xpath('string(//dt[@id="groups"]/following-sibling::dd[1])').get('').strip()
        synonymes_list = doc.xpath('//dt[@id="synonyms"]/following-sibling::dd[1]/ul/li')
        synonymes = self.parse_list(synonymes_list)
        indication_list = doc.xpath('//dt[@id="indication"]/following-sibling::dd[1]/p')
        indication = self.parse_list(indication_list)

        drug_categories_list = doc.xpath('//dt[@id="drug-categories"]/following-sibling::dd[1]//a')
        drug_categories = self.parse_list(drug_categories_list)

        chemical_formula = doc.xpath('//dt[@id="chemical-formula"]/following-sibling::dd[1]').get('').replace('</dd>',
                                                                                                              '').strip()
        chemical_formula = re.sub('(<dd .*?>)', '', chemical_formula)

        food_interaction_list = doc.xpath('//dt[@id="food-interactions"]/following-sibling::dd[1]//li')
        food_interaction = self.parse_list(food_interaction_list)

        toxicity_list = doc.xpath('//dt[@id="toxicity"]/following-sibling::dd[1]//p')
        toxicity = self.parse_list(toxicity_list)
        clearance_list = doc.xpath('//dt[@id="clearance"]/following-sibling::dd[1]//p')
        metabolism_list = doc.xpath('//dt[@id="metabolism"]/following-sibling::dd[1]//p')  # todo 数据有列表与文本
        half_life_list = doc.xpath('//dt[@id="half-life"]/following-sibling::dd[1]//p')
        clearance = self.parse_list(clearance_list)
        metabolism = self.parse_list(metabolism_list)
        half_life = self.parse_list(half_life_list)

        protein_binding_list = doc.xpath('//dt[@id="protein-binding"]/following-sibling::dd[1]//p')
        protein_binding = self.parse_list(protein_binding_list)
        volume_distribution_list = doc.xpath('//dt[@id="volume-of-distribution"]/following-sibling::dd[1]//p')
        volume_distribution = self.parse_list(volume_distribution_list)

        absorption_list = doc.xpath('//dt[@id="absorption"]/following-sibling::dd[1]//p')
        absorption = self.parse_list(absorption_list)

        pharmacodynamics_list = doc.xpath('//dt[@id="pharmacodynamics"]/following-sibling::dd[1]//p')
        pharmacodynamics = self.parse_list(pharmacodynamics_list)

        biologic_classification_1 = doc.xpath(
            '//dt[@id="biologic-classification"]/following-sibling::dd[1]/text()').get('').strip()
        biologic_classification_2 = doc.xpath(
            'string(//dt[@id="biologic-classification"]/following-sibling::dd[1]//span)').get('').strip()

        biologic_classification = [biologic_classification_1, biologic_classification_2]
        biologic_classification = [_ for _ in biologic_classification if _]

        sequences = doc.xpath('string(//dt[@id="sequences"]/following-sibling::dd[1]//pre)').get('').strip()

        structure = doc.xpath('//dt[@id="structure"]/following-sibling::dd[1]//a/@href').get('').strip()
        if structure and not structure.startswith('http'):
            structure = f'https://go.drugbank.com{structure}'

        pathways = doc.xpath('string(//dt[@id="pathways"]/following-sibling::dd[1]/span)').get('').strip()
        if pathways != 'Not Available':
            pathways = doc.xpath('//dt[@id="pathways"]/following-sibling::dd[1]').get('').replace('</dd>', '').strip()

        pharmacogenomic_effects = doc.xpath(
            'string(//dt[@id="pharmacogenomic-effects-adrs"]/following-sibling::dd[1]/span)').get('').strip()
        if pathways != 'Not Available':
            pharmacogenomic_effects = doc.xpath(
                '//dt[@id="pharmacogenomic-effects-adrs"]/following-sibling::dd[1]').get(
                '').replace('</dd>', '').strip()

        mechanism_action = self.parse_mechanism_action(doc)

        item = DrugBankHit(
            id=drug_id,
            name=name,
            brand_name=brand_name,
            summary=summary,
            synonymes=synonymes,
            generic_name=generic_name,
            background=background,
            type=type,
            groups=groups,
            indication=indication,
            drug_categories=drug_categories,
            chemical_formula=chemical_formula,
            pathways=pathways,
            pharmacogenomic_effects=pharmacogenomic_effects,
            mechanism_action=mechanism_action,
            food_interaction=food_interaction,
            toxicity=toxicity,
            pharmacodynamics=pharmacodynamics,
            biologic_classification=biologic_classification,
            sequences=sequences,
            structure=structure,
            absorption=absorption,
            volume_distribution=volume_distribution,
            protein_binding=protein_binding,
            clearance=clearance,
            metabolism=metabolism,
            half_life=half_life,
        )
        return item

    async def run(self):
        async for data in self.all():
            print(data)


if __name__ == '__main__':
    drug = DrugBank()
    import asyncio

    # res = asyncio.run(drug.get_data('DB09532'))
    res = asyncio.run(drug.get_data('DB00091'))
    print(res.json())
