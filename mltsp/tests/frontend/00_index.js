casper.test.begin('index loads'
                  /*, planned nr of tests, */,  function suite(test) {
    casper.start('http://localhost:5000', function() {
        test.assertTextExists('Please log in',
                              'Authentication displayed on index page');
    });

    casper.run(function() {
        test.done();
    });
});
