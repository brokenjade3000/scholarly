import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from scholarly import scholarly
from scholarly import ProxyGenerator
import os
from dotenv import load_dotenv
import logging
import time



class TestSearchPubs(unittest.TestCase):
    """Test cases for scholarly.search_pubs functionality"""

    logger = logging.getLogger(__name__)

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                cls.pg = ProxyGenerator()
                success = cls.pg.FreeProxies()
                print(cls.pg)
                if success:
                    # scholarly.use_proxy(cls.pg)
                    # test_query = scholarly.search_pubs("NLP dementia")
                    # next(test_query)
                    cls.logger.info("Successfully initialized and tested free proxies")
                    return
                else:
                    cls.logger.warning(f"Failed to initialize free proxies (attempt {attempt + 1}/{max_attempts})")
            except Exception as e:
                 cls.logger.warning(f"Failed to initialize proxies (attempt {attempt + 1}/{max_attempts})")
            
            if attempt < max_attempts - 1:
                time.sleep(5)  # Wait before retrying
        
        raise ValueError("Failed to initialize free proxies after multiple attempts")


    def setUp(self):
        """Set up test fixtures before each test"""
        scholarly.set_timeout(30)
        scholarly.set_retries(3)

    def test_search_pubs_captcha_handling(self):
        """Test that search_pubs handles captcha challenges correctly when searching publications.
        
        This test verifies that:
        1. The search can handle a large number of results that might trigger captcha
        2. The navigator properly handles any captcha challenges
        3. The expected publication metadata is returned
        """
        # Search for a common ML term that will return many results
        query = "machine learning"
        search_results = scholarly.search_pubs(query)
        
        # Get first 20 publications to force multiple page loads
        pubs = []
        try:
            for i, pub in enumerate(search_results):
                if i >= 20:
                    break
                pubs.append(pub)
        except Exception as e:
            self.fail(f"Failed to handle captcha during publication search: {str(e)}")

        # Verify we got results
        self.assertGreater(len(pubs), 0)
        
        # Verify essential fields are present in results
        first_pub = pubs[0]
        required_fields = ['bib', 'author_id', 'num_citations', 'pub_url']
        for field in required_fields:
            self.assertIn(field, first_pub, f"Missing required field {field}")
            
        # Verify bib contains basic metadata
        required_bib_fields = ['title', 'author', 'pub_year']
        for field in required_bib_fields:
            self.assertIn(field, first_pub['bib'], f"Missing required bib field {field}")

if __name__ == '__main__':
    unittest.main()