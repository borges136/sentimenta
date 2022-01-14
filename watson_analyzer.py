from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

class WatsonToneAnalyzer():
  def __init__(self, credentials_path= 'watson_credentials.json'):
    credentials = json.load(open(credentials_path))
    authenticator = IAMAuthenticator(credentials['apikey'])
    self.tone_analyzer = ToneAnalyzerV3(
      version='2017-09-21',
      authenticator=authenticator
    )

    self.tone_analyzer.set_service_url(credentials['url'])

  def analyze(self, text):
    tone_analysis = self.tone_analyzer.tone(
      {'text': text},
      content_type='application/json'
    ).get_result()
    # print(f'result from watson api: {json.dumps(tone_analysis, indent=2)}')
    return(tone_analysis)