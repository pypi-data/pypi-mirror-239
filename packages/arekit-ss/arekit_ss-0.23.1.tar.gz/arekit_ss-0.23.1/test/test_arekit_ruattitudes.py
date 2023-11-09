import unittest

from arekit.common.pipeline.base import BasePipeline
from arekit.contrib.source.ruattitudes.entity.parser import RuAttitudesTextEntitiesParser
from arekit.contrib.utils.data.writers.json_opennre import OpenNREJsonWriter

from arekit_ss.framework.arekit.rows_bert import create_bert_rows_provider
from arekit_ss.framework.arekit.rows_ru_sentiment_nn import create_ru_sentiment_nn_rows_provider
from arekit_ss.framework.arekit.serialize_bert import serialize_bert_pipeline
from arekit_ss.framework.arekit.serialize_nn import serialize_nn_pipeline

from arekit_ss.sources.config import SourcesConfig
from arekit_ss.sources.labels.scaler import PosNegNeuRelationsLabelScaler
from arekit_ss.sources.labels.scaler_frames import ThreeLabelScaler
from arekit_ss.sources.s_ruattitudes import build_ruattitudes_datapipeline
from arekit_ss.text_parser.text_lm import create_lm
from arekit_ss.text_parser.text_nn_ru_frames import create_nn_ru_frames


class TestRuAttitudes(unittest.TestCase):

    __output_dir = "_out/"

    def __config(self):
        cfg = SourcesConfig()
        cfg.docs_limit = 5
        cfg.dest_lang = "en"
        cfg.src_lang = "ru"
        return cfg

    def test_serialize_bert_opennre(self):
        cfg = self.__config()
        cfg.entities_parser = RuAttitudesTextEntitiesParser()
        cfg.text_parser = create_lm(cfg)
        data_folding, pipelines = build_ruattitudes_datapipeline(cfg)
        item = serialize_bert_pipeline(output_dir="_out/ra-bert",
                                       writer=OpenNREJsonWriter(text_columns=["text_a"]),
                                       rows_provider=create_bert_rows_provider(
                                           terms_per_context=100,
                                           labels_scaler=PosNegNeuRelationsLabelScaler()))
        s_ppl = BasePipeline([item])
        s_ppl.run(input_data=None,
                  params_dict={
                      "data_folding": data_folding,
                      "data_type_pipelines": pipelines
                  })

    def test_serialize_nn_csv(self):
        cfg = self.__config()
        cfg.entities_parser = RuAttitudesTextEntitiesParser()
        cfg.text_parser = create_nn_ru_frames(cfg)
        data_folding, pipelines = build_ruattitudes_datapipeline(cfg)
        item = serialize_nn_pipeline(output_dir="_out/ra-nn",
                                     writer=OpenNREJsonWriter(text_columns=["text_a"]),
                                     rows_provider=create_ru_sentiment_nn_rows_provider(
                                         relation_labels_scaler=PosNegNeuRelationsLabelScaler(),
                                         frame_roles_label_scaler=ThreeLabelScaler(),
                                         vectorizers="default"))
        s_ppl = BasePipeline([item])
        s_ppl.run(input_data=None,
                  params_dict={
                      "data_folding": data_folding,
                      "data_type_pipelines": pipelines
                  })

    def test_serialize_nn_opennre(self):
        cfg = self.__config()
        cfg.entities_parser = RuAttitudesTextEntitiesParser()
        cfg.text_parser = create_nn_ru_frames(cfg)
        data_folding, pipelines = build_ruattitudes_datapipeline(cfg)
        item = serialize_nn_pipeline(writer=OpenNREJsonWriter(text_columns=["text_a"]),
                                     output_dir="_out/ra-nn",
                                     rows_provider=create_ru_sentiment_nn_rows_provider(
                                         relation_labels_scaler=PosNegNeuRelationsLabelScaler(),
                                         frame_roles_label_scaler=ThreeLabelScaler(),
                                         vectorizers="default"))

        s_ppl = BasePipeline([item])
        s_ppl.run(input_data=None,
                  params_dict={
                      "data_folding": data_folding,
                      "data_type_pipelines": pipelines
                  })
